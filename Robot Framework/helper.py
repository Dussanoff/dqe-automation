import os
from datetime import datetime, timedelta

import robot.api.deco
from robot.libraries.BuiltIn import BuiltIn
import pandas as pd
import pyarrow.parquet as pq
from selenium.webdriver.common.by import By


class Helper:
    @robot.api.deco.keyword("Read HTML Table Into DF")
    def read_html_table_into_df(self, xPath, filter_date=None):
        driver = BuiltIn().get_library_instance("SeleniumLibrary").driver
        driver.set_window_size(1300, 900)
        return read_table(driver, xPath, filter_date=filter_date)


    @robot.api.deco.keyword("Read Parquet Dataset")
    def read_parquet_dataset(self, parquet_file, filter_date=None):
        path = os.path.abspath(parquet_file)
        if not os.path.isfile(path):
            raise ValueError(f"'{path}' is not a valid file.")

        df = pq.read_table(path).to_pandas()
        df = filter_df_by_date(df, filter_date) if filter_date else df
        return df


    @robot.api.deco.keyword("Compare DataFrames")
    def compare_dataframes(self, df1, df2):

        for col in df1.columns:
            df1[col] = df1[col].astype(str)

        for col in df2.columns:
            df2[col] = df2[col].astype(str)

        return pd.concat([df1, df2]).drop_duplicates(keep=False)



def read_table(driver, xPath, correct=True, filter_date=None):
    table = driver.find_element(By.XPATH, xPath)
    columns = table.find_elements(By.CSS_SELECTOR, "g.y-column")

    columns_dict = {}
    for column in columns:
        header = column.find_elements(By.CSS_SELECTOR, "g.column-block#header")[0].text
        cells_list = []
        column_blocks = column.find_elements(By.CSS_SELECTOR, "g.column-block[id^='cells']")
        column_blocks_sorted = sorted(column_blocks, key=lambda block: block.get_attribute("id"))
        for column_block in column_blocks_sorted:
            column_cells = column_block.find_elements(By.CLASS_NAME, "column-cell")
            column_cells_sorted = sorted(column_cells, key=lambda cell: cell.get_attribute("transform"))
            for column_cell in column_cells_sorted:
                cells_list.append(column_cell.text)
        columns_dict[header] = cells_list

    if not correct:
        for i in range(len(columns_dict.get("Visit Date"))):
            date = columns_dict["Visit Date"][i]
            new_date = datetime.strptime(date, "%Y-%m-%d").date() + timedelta(days=10)
            columns_dict["Visit Date"][i] = new_date.strftime("%Y-%m-%d")

    df = pd.DataFrame(columns_dict)
    df = filter_df_by_date(df, filter_date) if filter_date else df

    return df

def filter_df_by_date(df, date):
    filter_date = pd.to_datetime(date)
    df['Visit Date'] = pd.to_datetime(df['Visit Date'])
    return df[df['Visit Date'] == filter_date].reset_index(drop=True)

if __name__ == "__main__":
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from time import sleep

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(r"drivers\chromedriver.exe")

    driver = webdriver.Chrome(options=options, service=service)
    driver.get(f"file://{os.path.abspath('report.html')}")

    sleep(2)

    df_correct = read_table(driver, "//*[@class='table']")
    df_correct.to_parquet("parquet/table_correct.parquet", index=False)

    df_incorrect = read_table(driver, "//*[@class='table']", False)
    df_incorrect.to_parquet("parquet/table_incorrect.parquet", index=False)

    driver.quit()


# robot --pythonpath . --outputdir ./results test.robot


