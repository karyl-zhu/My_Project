import os
import requests
from bs4 import BeautifulSoup
import re
import datetime
import tarfile
import shutil

headers = {'User-Agent': 'Mozilla/5.0'}
base_url = 'https://tisvcloud.freeway.gov.tw/history/TDCS/M03A/'

# 建立最終資料夾
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
unzip_folder = os.path.join(parent_dir, 'Web_Crawler', '2025')
os.makedirs(unzip_folder, exist_ok=True)

# 正則比對檔名格式，抓月份與日期
pattern = re.compile(r'^M03A_2025(\d{2})(\d{2})\.tar\.gz$')

# 下載並解析網頁
res = requests.get(base_url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')

links = soup.find_all('a')
seen_files = set()  # 避免重複處理

count = 0  # 成功新增解壓的檔案數
skipped_count = 0  # 被跳過的檔案數

for link in links:
    try:
        href = link['href']

        if href in seen_files:
            continue
        seen_files.add(href)

        match = pattern.match(href)
        if not match:
            continue

        month, day = match.groups()
        date_str = f'2025-{month}-{day}'
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')

        # 只抓 週末 且 7 月 1 日以前的資料
        if date_obj.weekday() < 5:
            continue
        if date_obj >= datetime.datetime(2025, 7, 1):
            continue

        filename = href
        zip_path = os.path.join(unzip_folder, filename)
        folder_name = filename.replace('.tar.gz', '')
        final_folder_name = folder_name[-8:]  # 20250706
        final_extract_path = os.path.join(unzip_folder, final_folder_name)

        if os.path.exists(final_extract_path):
            skipped_count += 1
            print(f"✅ 已存在：{final_folder_name}，跳過")
            continue

        print(f"⬇️ 下載中：{filename}")
        res_file = requests.get(base_url + filename, stream=True)
        with open(zip_path, 'wb') as f:
            for chunk in res_file.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"📦 解壓縮：{filename}")
        with tarfile.open(zip_path, 'r:gz') as tar:
            tar.extractall(path=os.path.join(unzip_folder, folder_name))

        inner_path = os.path.join(unzip_folder, folder_name, 'M03A', final_folder_name)
        if os.path.exists(inner_path):
            shutil.move(inner_path, final_extract_path)
        else:
            print(f"⚠️ 找不到資料夾：{inner_path}")
            continue

        shutil.rmtree(os.path.join(unzip_folder, folder_name))
        os.remove(zip_path)

        count += 1
        print(f"✅ 已完成：{final_folder_name}")

    except Exception as e:
        print(f"⚠️ 發生錯誤：{href} - {e}")

print(f"\n🎉 全部完成：")
print(f"✅ 新增並解壓：{count} 筆")
print(f"⏩ 跳過（已存在）：{skipped_count} 筆")
