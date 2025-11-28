import re
import time
import os
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class SeleniumWebDriverContextManager:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(r"drivers\chromedriver.exe")

        self.driver = webdriver.Chrome(options=options, service=service)
        self.driver.set_window_size(1300, 900)

    def __enter__(self):
        return self.driver


    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()


def find_element_with_waits(driver, wait_time, poll_frequency, xPath=None, CSS=None):

    if xPath and CSS:
        raise Exception("Provided both xPath and CSS. Provide only one option.")
    if not xPath and not CSS:
        raise Exception("Provide at least one locator: xPath or CSS.")

    wait = WebDriverWait(driver, wait_time, poll_frequency=poll_frequency, ignored_exceptions=[TimeoutException])

    try:
        if xPath:
            element = wait.until(EC.visibility_of_element_located((By.XPATH, xPath)))
        else:
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, CSS)))
    except TimeoutException:
        raise Exception(f"Element not found using locator: xPath={xPath}, CSS={CSS}")

    return element


def table_interaction(driver, output_csv):
    table = find_element_with_waits(driver, 10, 5, xPath="//*[@class='table']")
    columns = table.find_elements(By.CSS_SELECTOR, "g.y-column")
    columns_dict = {}
    for column in columns:
        header = column.find_elements(By.CSS_SELECTOR, "g.column-block#header")[0].text
        cells_list = []
        column_blocks = column.find_elements(By.CSS_SELECTOR, "g.column-block[id^='cells']")
        for column_block in column_blocks:
            column_cells = column_block.find_elements(By.CLASS_NAME, "column-cell")
            for column_cell in column_cells:
                cells_list.append(column_cell.text)
        columns_dict[header] = cells_list

    df = pd.DataFrame(columns_dict)
    df.to_csv(output_csv, index=False, encoding="utf-8-sig")

def doughnut_chart_interaction(driver, output):
    n = 0
    os.makedirs(output, exist_ok=True)

    groups = find_element_with_waits(driver, 10, 5, xPath="//*[@class='groups']")
    driver.save_screenshot(os.path.join(output, f"screenshot{n}.png"))
    doughnut_list = doughnut_chart_extract(driver)

    df = pd.DataFrame(doughnut_list[1:], columns=doughnut_list[0])
    df.to_csv(f"{output}/{output}{n}.csv", index=False, encoding="utf-8-sig")

    traces = groups.find_elements(By.CSS_SELECTOR, "g.traces")

    for trace in traces:
        try:
            trace.click()
        except Exception as e:
            print(f"Failed to click {trace.text}: {e}")
            continue
        time.sleep(0.3)
        n += 1
        driver.save_screenshot(os.path.join(output, f"screenshot{n}.png"))
        doughnut_list = doughnut_chart_extract(driver)

        df = pd.DataFrame(doughnut_list[1:], columns=doughnut_list[0])
        df.to_csv(f"{output}/{output}{n}.csv", index=False, encoding="utf-8-sig")

        try:
            trace.click()
        except Exception as e:
            print(f"Failed to click {trace.text}: {e}")
            continue

        time.sleep(0.3)


def doughnut_chart_extract(driver):
    pielayer = find_element_with_waits(driver, 10, 5, xPath="//*[@class='trace']")
    slicetexts = pielayer.find_elements(By.XPATH, "//*[name()='text' and @class='slicetext']")
    doughnut_list = [["Facility Type", "Min average time spent by Facility Type for the last week"]]

    for slicetext in slicetexts:
        doughnut_slice = []
        lines = slicetext.find_elements(By.CSS_SELECTOR, "tspan.line")
        for line in lines:
            doughnut_slice.append(line.text)
        doughnut_list.append(doughnut_slice)

    return doughnut_list




if __name__ == "__main__":
    file_path = os.path.abspath("report.html")

    with SeleniumWebDriverContextManager() as driver:
        driver.get(f"file://{file_path}")
        table_interaction(driver, "table.csv")
        doughnut_chart_interaction(driver, "doughnut")