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
import dask.dataframe as ddf
from math import sqrt
from pqdm.processes import pqdm
from joblib import Parallel, delayed
from tqdm import tqdm

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="./chromedriver.exe")

# baseUrl = "https://hethongphapluat.com/hoi-dap-phap-luat_page-{}.html"


def crawl_each_link(url):
    driver.get(url)
    wait = WebDriverWait(driver, 1)
    temp_df = pd.DataFrame(columns=["url", "question", "long_question",])
    content = driver.find_element(By.XPATH, "//div[@class='panel-body']")

    return content.text

df = pd.read_csv("./raw_data/raw_HeThongPhapLuat_ANS.csv", index_col=0)
df = df[:100]

def crawl_parallel(i):
    content = crawl_each_link(df.iloc[i]['url'])
    # print("this is number ", i)
    df.at[i, 'long_answer'] = content
    # print(df.at[i, 'long_answer'])
    return content

def crawl_dask(arg):
    idx, row = arg
    content = crawl_each_link(row['url'])
    return content


result = pqdm(range(0, 100), crawl_parallel, n_jobs=5)


df.to_csv("./raw_data/raw_HeThongPhapLuat_ANS_ff.csv")
# if __name__ == '__main__':
    # t_url = "https://hethongphapluat.com/bi-lua-mat-tien-phai-lam-nhu-the-nao.html"
    # crawl_each_link(t_url)


    # df['long_answer'] = pd.NA

    # df = df.dropna(subset=['url'])
    # print(df['long_answer'].isna().sum())
    # df = df.reset_index(drop=True)
    # df.to_csv("./raw_data/raw_HeThongPhapLuat_ANS.csv")
    # df['long_answer'] = df['long_answer'].astype(str)


    try:
        for i in tqdm(range(55, len(df))):
            content = crawl_each_link(df.iloc[i]['url'])
            df.at[i, 'long_answer'] = content
        # result = pqdm(range(0, 100), crawl_parallel, n_jobs=5)
        df['long_answer'] = result
        driver.close()
        print("Good job! Done and saving to csv")
        df.to_csv("./raw_data/raw_HeThongPhapLuat_ANS_ff.csv")
        # print(result)
    except Exception as e:
        print(e)
        # print("ERROR DUMP at index {}! Saving to csv".format(i));
        print(result)
        df.to_csv("./raw_data/raw_HeThongPhapLuat_ANS.csv")

    # df_dask = ddf.from_pandas(df, npartitions=12)
    # df_dask['long_answer'] = df_dask.apply(lambda x: crawl_parallel(x), meta=('str')).compute(scheduler='multiprocessing')
    # df = pd.DataFrame(df_dask)
    # df.to_csv('./raw_data/test_parallel')



