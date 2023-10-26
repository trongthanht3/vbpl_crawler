import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import winsound

from tqdm import tqdm
import json
import pandas as pd
import time

options = Options()
options.add_argument("--incognito")
options.add_argument("--window-size=1920x1080")
# options.add_argument("start-maximized")
# options.add_argument("enable-automation")
# options.add_argument("--headless")
options.add_argument("--disable-extensions");
options.add_argument("--dns-prefetch-disable");
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)


def crawl_text(url):
    try:
        driver.get(url)
        WebDriverWait(driver, 0.2)
    # driver.set_page_load_timeout(5)

        driver.set_page_load_timeout(5)
        content = driver.find_element(By.XPATH, '//*[@id="toanvancontent"]')
        text = content.text
        text = text.replace("  ", "")
        return text
    except Exception as e:
        print(e)
        return ""


if __name__ == '__main__':
    df = pd.read_csv("./raw_data/df_law_corpus_soft_processed.csv")
    df['content'] = df['content'].astype(str)
    # content = crawl_text(df.at[0, "url"])
    # print(content)
    try:
        for i in tqdm(range(350, len(df))):
            content = crawl_text(df.iloc[i]["url"])
            df.at[i, "content"] = content
            if content != "":
                df.at[i, "is_content"] = True
            # temp_d = crawl_vbpl_each_link_text_only(i)
            # df = pd.concat([df, temp_d])
        driver.close()
        print("Good job! Done and saving to csv")
        df.to_csv("./raw_data/df_law_corpus_soft_processed.csv", index=False)
    except Exception as e:
        print(e)
        print("ERROR DUMP at index {}! Saving to csv".format(i))
        df.to_csv("./raw_data/df_law_corpus_soft_processed.csv", index=False)
        winsound.PlaySound("./oof.mp3", winsound.SND_ALIAS)
    except KeyboardInterrupt:
        print(e)
        print("ERROR DUMP at index {}! Saving to csv".format(i))
        df.to_csv("./raw_data/df_law_corpus_soft_processed.csv", index=False)
        winsound.PlaySound("./oof.mp3", winsound.SND_ALIAS)
