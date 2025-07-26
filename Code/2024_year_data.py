# 2024年高工局所有車流資料下載

# 操作、建立資料夾 
import os
# 網頁爬蟲
import requests
from bs4 import BeautifulSoup
# 正規表達式
import re
# 解壓縮檔案
import tarfile

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'}
base_url = 'https://tisvcloud.freeway.gov.tw/history/TDCS/M03A/'

# os.getcwd() -> 取得當前工作目錄
# os.path.join -> 合併路徑，使用這與法能讓不同系統的電腦不會因為路徑顯示方式不同而出錯
# os.makedirs -> 建立資料夾
save_folder = os.path.join(os.getcwd(), 'Web_Crawler', '2024', 'zip file')
os.makedirs(save_folder, exist_ok=True)

# 確保資料夾存在
os.makedirs(save_folder, exist_ok=True)

# 發送請求並解析 HTML
res = requests.get(base_url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
links = soup.find_all('td', attrs={'class': 'indexcolname'})

# 設定變數，此變數為 2024 年的檔案
data_2024 = re.compile(r'^M03A_2024\d{4}\.tar\.gz$')

count = 0
for link in links:
    try:
        # 抓這段 links 裡 <a> 標籤的 href 屬性
        href = link.a['href']

        if not data_2024.match(href):
            continue  # 不符合2024年的資料就跳過

        file_url = base_url + href
        # 用os.path.join 避免不同的作業系統導致路徑符號錯誤
        save_path = os.path.join(save_folder, href)

        # 把剛剛 file_url 拿到的網址透過get請求把這網頁的資料抓下來丟在 file_res 變數裡
        file_res = requests.get(file_url)
        # 打開剛剛設定好的電腦路徑;wb->二進位寫入模式
        # with 是 Python 的語法糖，用來自動開關檔案，確保寫完檔案後會正常關閉。
        with open(save_path, 'wb') as f:
            # 把從網路抓回來的檔案內容寫進剛剛打開的本地檔案。
            f.write(file_res.content)

        count += 1
        print(f"[{count}] 已下載：{href}")

    except Exception as e:
        print(f"⚠️ 錯誤：下載 {href} 時發生錯誤：{e}")