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

options = Options()
options.add_argument("--incognito")
options.add_argument("--window-size=1920x1080")
# options.add_argument("enable-automation")
# options.add_argument("--headless")
# options.add_argument("--disable-extensions");
# options.add_argument("--dns-prefetch-disable");
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--disable-browser-side-navigation")
# options.add_argument("--disable-gpu")
driver = webdriver.Chrome(chrome_options=options, executable_path="./chromedriver.exe")


def crawl_url(page):
    url = "https://vbpl.vn/VBQPPL_UserControls/Publishing_22/TimKiem/p_KetQuaTimKiemVanBan.aspx??type=0&s=0&SearchIn=VBPQFulltext&&IsVietNamese=True&DivID=tabVB_lv1_01&Page={}&RowPerPage=1000".format(
        page)
    driver.set_page_load_timeout(1000)
    driver.get(url)

    temp_df = pd.DataFrame(columns=["url", "lawName", "description", "expDate", "isExpire"])

    title = driver.find_elements(By.XPATH, '//ul[@class="listLaw"]/li')

    for tit in title:
        des = tit.find_element(By.XPATH, './/div[@class="des"]')
        law_name = tit.find_element(By.XPATH, './/p[@class="title"]')
        url = law_name.find_element(By.XPATH, './/a')
        exp_date = tit.find_elements(By.XPATH, './/p[@class="green"]')[-1]
        try:
            is_expire = tit.find_element(By.XPATH, './/p[@class="red"]').text
        except:
            pass
            is_expire = pd.NA
        #         seri = pd.Series(data = {
        #                             'url':url.get_attribute('href'),
        #                             'law_name': law_name.text,
        #                             'description': des.text
        #                          },
        #                          index=['url', 'law_name', 'description'])
        temp_df = temp_df.append({
            'url': url.get_attribute('href'),
            'lawName': law_name.text,
            'description': des.text,
            "expDate": exp_date.text,
            "isExpire": is_expire
        }, ignore_index=True)
    return temp_df




if __name__ == '__main__':
    df = pd.DataFrame(columns=['url', 'law_name', 'description'])

    list_raw_data = os.listdir("./raw_data")
    if "raw_VBPL_corpus.csv" not in list_raw_data:
        df.to_csv("./raw_data/raw_VBPL_corpus.csv")
    else:
        df = pd.read_csv("./raw_data/raw_VBPL_corpus.csv", index_col=0)

    try:
        for i in tqdm(range(1, 140)):
            temp_d = crawl_url(i)
            df = pd.concat([df, temp_d])
        driver.close()
        print("Good job! Done and saving to csv")
        df.to_csv("./raw_data/raw_VBPL_corpus.csv")
    except Exception as e:
        print(e)
        print("ERROR DUMP at index {}! Saving to csv".format(i));
        df.to_csv("./raw_data/raw_VBPL_corpus.csv")
