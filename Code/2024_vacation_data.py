# 2024年假日車流資料下載
import os
import requests
from bs4 import BeautifulSoup
import re
import datetime

headers = {'User-Agent': 'Mozilla/5.0'}
base_url = 'https://tisvcloud.freeway.gov.tw/history/TDCS/M03A/'

# 取得當前執行此 Python 檔案的資料夾
script_dir = os.path.dirname(os.path.abspath(__file__))
# 取得上層資料夾
parent_dir = os.path.dirname(script_dir)
# 在上層建資料夾                   
save_folder = os.path.join(parent_dir, 'Web_Crawler', '2024', 'zip_file')

os.makedirs(save_folder, exist_ok=True)

res = requests.get(base_url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
links = soup.find_all('td', attrs={'class': 'indexcolname'})

# 改成這樣可以可以用 .match() 抓出：
# (\d{2}) 第一段 → 月份
# (\d{2}) 第二段 → 日期
# 後續才可以勾出假日的時段
data_2024 = re.compile(r'^M03A_2024(\d{2})(\d{2})\.tar\.gz$')

count = 0
for link in links:
    try:
        href = link.a['href']
        # 這邊改寫法是為了方便後面進一步比對月份跟日期
        # 此處依舊是先比對是否為 2024 年的資料 -> data_2024
        # 也可以用原本的方式寫，先過濾2024年後，再繼續用 if 迴圈過濾月分和日子
        match = data_2024.match(href)

        if not match:
            continue

        # 這行是從前面的 re.match 結果中取出「月份」與「日期」。
        # 第一個 \d{2} 是月份，例如 "01" 到 "12"。
        # 第二個 \d{2} 是日期，例如 "01" 到 "31"。
        # month, day = match.groups() 會將這兩個值拆開並賦值給 month 和 day 兩個變數。
        month, day = match.groups()
        date_str = f'2024-{month}-{day}'
        # 這行是把字串轉成一個 Python 的「日期物件」，方便進一步做日期相關運算。
        # 主要是跟.weekday()使用語法有關
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')

        # 這裡用 .weekday() 來判斷是不是週末（週一是0，週日是6）。
        # 如果是 0～4（週一到週五），就跳過，保留六日。
        if date_obj.weekday() < 5:
            continue

        file_url = base_url + href
        save_path = os.path.join(save_folder, href)

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