import os
import requests
from bs4 import BeautifulSoup
import re
import datetime

headers = {'User-Agent': 'Mozilla/5.0'}
base_url = 'https://tisvcloud.freeway.gov.tw/history/TDCS/M03A/'

save_folder = os.path.join(os.getcwd(), 'Web_Crawler', '2025', 'zip_file')
os.makedirs(save_folder, exist_ok=True)

res = requests.get(base_url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
links = soup.find_all('td', attrs={'class': 'indexcolname'})

data_2025 = re.compile(r'^M03A_2025(\d{2})(\d{2})\.tar\.gz$')

count = 0
for link in links:
    try:
        href = link.a['href']
        match = data_2025.match(href)

        if not match:
            continue

        month, day = match.groups()
        date_str = f'2025-{month}-{day}'
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')

        # 加入只抓週末
        if date_obj.weekday() < 5:
            continue

        file_url = base_url + href
        save_path = os.path.join(save_folder, href)

        # 只抓7月之前(含6月)的檔案
        if date_obj.month > 6:
            continue

        # 如果下載地點已經存在這檔案，就會跳過
        if os.path.exists(save_path):
            print(f"[{count}] 已存在，跳過：{href}")
            continue

        file_res = requests.get(file_url, stream=True)
        with open(save_path, 'wb') as f:
            for chunk in file_res.iter_content(chunk_size=8192):
                f.write(chunk)

        count += 1
        print(f"[{count}] 已下載：{href}")

    except Exception as e:
        print(f"⚠️ 錯誤：下載 {href} 時發生錯誤：{e}")

print(f"✅ 全部完成，共下載 {count} 筆檔案")