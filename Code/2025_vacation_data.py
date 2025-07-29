import os
import requests
from bs4 import BeautifulSoup
import re
import datetime
import tarfile
import shutil

headers = {'User-Agent': 'Mozilla/5.0'}
base_url = 'https://tisvcloud.freeway.gov.tw/history/TDCS/M05A/'

save_folder = os.path.join(os.getcwd(), 'Web_Crawler', '2025', 'zip_file')
os.makedirs(save_folder, exist_ok=True)

res = requests.get(base_url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
links = soup.find_all('td', attrs={'class': 'indexcolname'})

data_2025 = re.compile(r'^M05A_2025(\d{2})(\d{2})\.tar\.gz$')

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

        # 只抓週末
        if date_obj.weekday() < 5:
            continue

        # 只抓1~6月
        if date_obj.month > 6:
            continue

        file_url = base_url + href
        save_path = os.path.join(save_folder, href)

        # 如果壓縮檔已存在，跳過下載及解壓
        if os.path.exists(save_path):
            print(f"[{count}] 壓縮檔已存在，跳過：{href}")
            continue

        print(f"⬇️ 下載中：{href}")
        file_res = requests.get(file_url, stream=True)
        with open(save_path, 'wb') as f:
            for chunk in file_res.iter_content(chunk_size=8192):
                f.write(chunk)

        # 解壓縮路徑
        folder_name = href.replace('.tar.gz', '')
        extract_path = os.path.join(save_folder, folder_name)

        print(f"📦 解壓縮：{href} 到 {extract_path}")
        with tarfile.open(save_path, 'r:gz') as tar:
            tar.extractall(path=extract_path)

        # 解壓完成刪除壓縮檔
        os.remove(save_path)

        count += 1
        print(f"[{count}] 已下載並解壓：{folder_name}")

    except Exception as e:
        print(f"⚠️ 錯誤：下載或解壓 {href} 時發生錯誤：{e}")

print(f"✅ 全部完成，共下載並解壓 {count} 筆檔案")
