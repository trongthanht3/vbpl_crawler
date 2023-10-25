import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tqdm import tqdm
import json
import pandas as pd
import time

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="./chromedriver.exe")

baseUrl = "https://hethongphapluat.com/hoi-dap-phap-luat_page-{}.html"


def crawl_URL_Question(data: pd.DataFrame, url):
    driver.get(url)
    wait = WebDriverWait(driver, 3)
    temp_df = pd.DataFrame(columns=["url", "question", "long_question"])
    title = driver.find_elements(By.XPATH, '//div[@class="panel panel-default"]')
    for panel in title:
        tit = panel.find_element(By.XPATH, './/h2')
        link = panel.find_element(By.XPATH, ".//a")
        long_question = panel.find_elements(By.XPATH, './/div[@class="panel-body"]//p[@class="justify"]//i')[-1]

        seri = pd.Series(data={
                                    'url': link.get_attribute('href'),
                                    'question': tit.text,
                                    'long_question': long_question.text
                                },
                        index = ['url', 'question', 'long_question'])
        temp_df = temp_df.append(seri, ignore_index=True)

        # print(tit.text)
        # print(link.get_attribute('href'))
        # print(long_question.text)
        # print("------------------------------------")

    return temp_df


if __name__ == '__main__':
    df = pd.DataFrame(columns=["url", "question", "long_question"])

    list_raw_data = os.listdir("./raw_data")
    if "raw_HeThongPhapLuat.csv" not in list_raw_data:
        df.to_csv("./raw_data/raw_HeThongPhapLuat.csv")
    else:
        df = pd.read_csv("./raw_data/raw_HeThongPhapLuat.csv", index_col=0)

    try:
        for i in tqdm(range(1100, 1603)):
            temp_d = crawl_URL_Question("", baseUrl.format(str(i)))
            df = pd.concat([df, temp_d])
        driver.close()
        print("Good job! Done and saving to csv")
        df.to_csv("./raw_data/raw_HeThongPhapLuat.csv")
    except Exception as e:
        print(e)
        print("ERROR DUMP at index {}! Saving to csv".format(i));
        df.to_csv("./raw_data/raw_HeThongPhapLuat.csv")
