import os
import pandas as pd
from sqlalchemy import create_engine

# 資料夾路徑
data_folder = os.path.join(os.getcwd(), 'data_clean', '2024')

# 資料庫連線資訊
db_user = 'root'
db_password = 'password'
db_host = '127.0.0.1'
db_port = '3306'
db_name = 'traffic_data'

# 建立 SQLAlchemy engine
engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4')

total_files = 0
success_count = 0

for dirpath, _, filenames in os.walk(data_folder):
    for file in filenames:
        if file.endswith('.csv'):
            file_path = os.path.join(dirpath, file)
            try:
                print(f"開始處理檔案: {file_path}")
                df = pd.read_csv(file_path)

                try:
                    # 確保欄位格式正確
                    df['TimeStamp'] = pd.to_datetime(df['TimeStamp'])
                    df['Date'] = pd.to_datetime(df['Date']).dt.date
                    df['Time'] = pd.to_datetime(df['Time']).dt.time
                except Exception as e:
                    print(f"⚠️ 時間欄位格式轉換失敗: {file_path}")
                    print(f"錯誤訊息: {e}")
                    continue  # 當欄位轉換失敗就跳過此檔案

                try:
                    # 匯入資料庫（append 模式）
                    df.to_sql('clean_data', con=engine, if_exists='append', index=False)
                    print(f"✅ 匯入成功: {file_path}")
                    success_count += 1
                except Exception as e:
                    print(f"❌ 資料庫匯入失敗: {file_path}")
                    print(f"錯誤訊息: {e}")

            except Exception as e:
                print(f"❌ 讀取檔案失敗: {file_path}")
                print(f"錯誤訊息: {e}")

            total_files += 1

print(f"\n✅ 匯入完成！總共處理 {total_files} 個檔案，成功匯入 {success_count} 個。")
