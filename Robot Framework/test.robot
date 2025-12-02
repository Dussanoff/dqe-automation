*** Settings ***
Library         SeleniumLibrary
Library         OperatingSystem
Library         helper.Helper
Test Setup      Open Browser With Options
Test Teardown   Close Browser

*** Variables ***
${DRIVER}           ${CURDIR}${/}drivers${/}chromedriver.exe
${URL}              file://${CURDIR}/report.html
${XPATH}            //*[@class='table']
${PARQUET_FOLDER}   parquet
${FILTER_DATE}      2025-11-23

*** Keywords ***
Open Browser With Options
    ${chrome_options}=  Evaluate        selenium.webdriver.ChromeOptions()  modules=selenium.webdriver
    Call Method     ${chrome_options}   add_argument    --headless
    Call Method     ${chrome_options}   add_argument    --disable-gpu
    Call Method     ${chrome_options}   add_argument    --no-sandbox
    Call Method     ${chrome_options}   add_argument    --disable-dev-shm-usage
    Open Browser    ${URL}    Chrome    executable_path=${DRIVER}   options=${chrome_options}

Read HTML Table With Retry
    [Arguments]     ${locator}  ${filter_date}=None
    ${dataframe}=   Wait Until Keyword Succeeds  15s  2s  Read HTML Table Into DF  ${locator}  ${filter_date}
    RETURN          ${dataframe}

Validate Parquet File
    [Arguments]     ${html_df}  ${parquet_file}  ${filter_date}=None
    ${parquet_df}=  Read Parquet Dataset    ${parquet_file}     ${FILTER_DATE}
    ${diff}=        Compare DataFrames      ${html_df}          ${parquet_df}
    Should Be True  ${diff.empty}    msg=Differences found in file '${parquet_file}':\n${diff}


*** Test Cases ***
Validate DataFrames
    ${html_df}=     Read HTML Table With Retry  ${XPATH}
    @{files}=       List Files In Directory     ${PARQUET_FOLDER}    pattern=*.parquet
    FOR  ${file}  IN  @{files}
        ${file_path}=   Join Path               ${PARQUET_FOLDER}   ${file}
        Run Keyword     Validate Parquet File   ${html_df}    ${file_path}
    END

Validate Filtered Parquet Files
    ${html_df}=     Read HTML Table With Retry  ${XPATH}            ${FILTER_DATE}
    @{files}=       List Files In Directory     ${PARQUET_FOLDER}    pattern=*.parquet
    FOR  ${file}  IN  @{files}
        ${file_path}=   Join Path               ${PARQUET_FOLDER}   ${file}
        Run Keyword     Validate Parquet File   ${html_df}    ${file_path}    ${FILTER_DATE}
    END


Validate one DataFrame
    ${html_df}=     Read HTML Table With Retry  ${XPATH}
    @{files}=       List Files In Directory     ${PARQUET_FOLDER}    pattern=*table_correct.parquet
    FOR  ${file}  IN  @{files}
        ${file_path}=   Join Path               ${PARQUET_FOLDER}   ${file}
        Run Keyword     Validate Parquet File   ${html_df}    ${file_path}
    END

Validate one Filtered Parquet Files
    ${html_df}=     Read HTML Table With Retry  ${XPATH}            ${FILTER_DATE}
    @{files}=       List Files In Directory     ${PARQUET_FOLDER}    pattern=*table_correct.parquet
    FOR  ${file}  IN  @{files}
        ${file_path}=   Join Path               ${PARQUET_FOLDER}   ${file}
        Run Keyword     Validate Parquet File   ${html_df}    ${file_path}    ${FILTER_DATE}
    END