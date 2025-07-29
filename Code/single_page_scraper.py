import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'}
url = 'https://tisvcloud.freeway.gov.tw/history/TDCS/M03A/20250722/00/'
res = requests.get(url, headers = headers)
soup = BeautifulSoup(res.text, 'html.parser')

links = soup.find_all('td', attrs={'class': 'indexcolname'})

for all_links in links:
    # print('https://tisvcloud.freeway.gov.tw/history/TDCS/M03A/20250722/00/' + all_links.a['href'])
    res = requests.get('https://tisvcloud.freeway.gov.tw/history/TDCS/M03A/20250722/00/' + all_links.a['href'])
    filename = all_links.a['href'].split('/')[-1]
    import os
    save_path = os.path.join('C:\\Users\\qj860\\Desktop\\專題\\爬蟲資料', filename)
    with open(save_path, 'wb') as f:
        f.write(res.content)

# import os
# import requests
# from bs4 import BeautifulSoup

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
# }
# base_url = 'https://tisvcloud.freeway.gov.tw/history/TDCS/M03A/20250722/00/'
# save_folder = r'C:\Users\qj860\Desktop\專題\爬蟲資料'

# # 確保資料夾存在
# os.makedirs(save_folder, exist_ok=True)

# # 發送請求並解析 HTML
# res = requests.get(base_url, headers=headers)
# soup = BeautifulSoup(res.text, 'html.parser')
# links = soup.find_all('td', attrs={'class': 'indexcolname'})

# # 下載每個連結的檔案
# for i, link in enumerate(links, 1):
#     try:
#         href = link.a['href']
#         file_url = base_url + href
#         filename = href.split('/')[-1]
#         save_path = os.path.join(save_folder, filename)

#         file_res = requests.get(file_url)
#         with open(save_path, 'wb') as f:
#             f.write(file_res.content)

#         print(f"[{i}/{len(links)}] 已下載：{filename}")

#     except Exception as e:
#         print(f"⚠️ 錯誤：下載 {href} 時發生錯誤：{e}")
