import pandas as pd
# pathlib 是 Python 內建（從 Python 3.4 開始有）的模組，專門用來操作檔案與資料夾路徑的工具。
# 用物件導向的方式來表示與操作路徑。
from pathlib import Path

file_path = r"C:\Users\qj860\Desktop\project\Web_Crawler\2024\20240106\00\TDCS_M03A_20240106_000000.csv"
# 由於原資料內並沒有設定欄位，以下欄位名稱為高公局定義的欄位名稱
cols = ['TimeStamp', 'GantryID', 'Direction', 'VehicleType', 'Volume']
# header=None 是告訴 pandas 此表格沒有欄位名稱，不要把第一列當欄位名稱
df = pd.read_csv(file_path,  header=None, names=cols)

# Direction N -> 北向(宜蘭往頭城)的車子
# df[條件篩選]
northbound_cars = df[df['Direction'] == 'N']
print(northbound_cars)

# 僅將 GantryID 分組後，加總 Volume
# Gantry_Volume = df.groupby('GantryID')['Volume'].sum().reset_index()

# 使用 groupby 將不同門架的資料分組
# .agg -> 對分組後的資料，針對不同欄位進行彙總/統計運算，語法如下
# df.groupby('欄位').agg({
#     '欄位1': '運算方法1',
#     '欄位2': '運算方法2',
#     ...
# })
# .rese_index() -> 彙總/計算後的資料建一個新的index
# 沒使用的話 groupby 所分組的欄位會變成 index，會影響後續資料的操作
Gantry_Volume = northbound_cars.groupby('GantryID').agg({
    'Volume':'sum',
    'Direction': 'first'  
}).reset_index()
 
print(Gantry_Volume)
