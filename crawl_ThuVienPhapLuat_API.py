import requests
import json
import pandas as pd

url = "https://hoidap.thuvienphapluat.vn/BaiVietMoi/Search"

payload = "page=1"
headers = {
  'authority': 'hoidap.thuvienphapluat.vn',
  'accept': '*/*',
  'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7,fr-FR;q=0.6,fr;q=0.5,zh-CN;q=0.4,zh;q=0.3',
  'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'cookie': 'G_ENABLED_IDPS=google; __zlcmid=1DWlSmI3BBtvf4h; Culture=vi; __utma=173276988.1664568398.1671016312.1671016312.1672496295.2; __utmz=173276988.1672496295.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _ga_PGVTRDMJGD=GS1.1.1672496294.2.1.1672506615.60.0.0; ASP.NET_SessionId=xp5qj4iqxhun2mv2foibewsk; _ga=GA1.2.586299448.1671016312; _gid=GA1.2.1520923501.1672887488; _gat_gtag_UA_109062685_1=1; _gat_gtag_UA_4355683_16=1; __atuvc=25%7C1; __atuvs=63b63cdf06ebb7bc018',
  'origin': 'https://hoidap.thuvienphapluat.vn',
  'referer': 'https://hoidap.thuvienphapluat.vn/bai-viet-moi',
  'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
  'x-requested-with': 'XMLHttpRequest'
}

response = requests.request("POST", url, headers=headers, data=payload)

raw_json = json.loads(response)
df = pd.json_normalize(raw_json)


