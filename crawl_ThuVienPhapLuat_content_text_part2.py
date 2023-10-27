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


# let's crawl on thuvienphapluat again
def crawl_text(law_name):
    try:
        url = "https://thuvienphapluat.vn/page/tim-van-ban.aspx?keyword={}".format(law_name)
        driver.get(url)
        # WebDriverWait(driver, 0.2)
        driver.set_page_load_timeout(20)
        try:
            content = driver.find_element(By.XPATH, '//*[@id="block-info-advan"]/div[2]/div[1]/div[1]/div[2]/p[1]/a')
        except:
            content = driver.find_element(By.XPATH,
                                          '/html/body/form/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[2]/td[1]/div[1]/div[4]/div[2]/div[2]/div[1]/div[2]/p[1]/a')

        url2 = content.get_attribute('href')
        driver.get(url2)
        content = driver.find_element(By.XPATH,
                                      '/html/body/form/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div/div[1]/div[2]/div[2]/div/div[1]/div')

        text = content.text
        text = text.replace("  ", "")
        return text
    except Exception as e:
        print(e)
        return ""


if __name__ == '__main__':
    df = pd.read_csv("./raw_data/no_content_part2_smaller.csv")
    df['content'] = df['content'].astype(str)
    # content = crawl_text(df.at[0, "url"])
    # print(content)
    try:
        for i in tqdm(range(0, len(df))):
            time.sleep(2)
            content = crawl_text(df.iloc[i]["lawName"])
            df.at[i, "content"] = content
            if content != "":
                df.at[i, "is_content"] = True
            # temp_d = crawl_vbpl_each_link_text_only(i)
            # df = pd.concat([df, temp_d])
        driver.close()
        print("Good job! Done and saving to csv")
        df.to_csv("./raw_data/no_content_part2_smaller.csv", index=False)
    except Exception as e:
        print(e)
        print("ERROR DUMP at index {}! Saving to csv".format(i))
        df.to_csv("./raw_data/no_content_part2_smaller.csv", index=False)
        winsound.PlaySound("./oof.mp3", winsound.SND_ALIAS)
    except KeyboardInterrupt:
        print("ERROR DUMP at index {}! Saving to csv".format(i))
        df.to_csv("./raw_data/no_content_part2_smaller.csv", index=False)
        winsound.PlaySound("./oof.mp3", winsound.SND_ALIAS)
