from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import pandas as pd
import time

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="./chromedriver.exe")

def crawlType(data, url):
    url = "https://hethongphapluat.com/hoi-dap-phap-luat_page-1603.html"
    driver.get(url)
    wait = WebDriverWait(driver, 3)

    title = driver.find_elements(By.XPATH, '//div[@class="panel panel-default"]')
    for panel in title:
        tit = panel.find_element(By.XPATH, './/h2')
        link = panel.find_element(By.XPATH, ".//a")
        print(tit.text)
        print(link.get_attribute('href'))


crawlType("","")

# with open('data/type.json', 'r', encoding='latin-1') as f:
#     links = json.load(f)
#
# for link in links:
#     data = []
#     crawlType(data, link['type_url'])
#     df = pd.DataFrame(data).to_json('./data/'+link['type_name']+'.json', orient='records')


driver.close()