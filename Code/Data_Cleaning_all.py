import pandas as pd
from pathlib import Path

# 你指定的 2024 年的所有有效日期 (用 YYYYMMDD 格式)
dates = [
    "20240106", "20240107", "20240113", "20240114", "20240120", "20240121", "20240127", "20240128",
    "20240203", "20240204", "20240210", "20240211", "20240217", "20240218", "20240224", "20240225",
    "20240302", "20240303", "20240309", "20240310", "20240316", "20240317", "20240323", "20240324", "20240330", "20240331",
    "20240406", "20240407", "20240413", "20240414", "20240420", "20240421", "20240427", "20240428",
    "20240504", "20240505", "20240511", "20240512", "20240518", "20240519", "20240525", "20240526",
    "20240601", "20240602", "20240608", "20240609", "20240615", "20240616", "20240622", "20240623", "20240629", "20240630",
    "20240706", "20240707", "20240713", "20240714", "20240720", "20240721", "20240727", "20240728",
    "20240803", "20240804", "20240810", "20240811", "20240817", "20240818", "20240824", "20240825", "20240831",
    "20240901", "20240907", "20240908", "20240914", "20240915", "20240921", "20240922", "20240928", "20240929",
    "20241005", "20241006", "20241012", "20241013", "20241019", "20241020", "20241026", "20241027",
    "20241102", "20241103", "20241109", "20241110", "20241116", "20241117", "20241123", "20241124", "20241130",
    "20241201", "20241207", "20241208", "20241214", "20241215", "20241221", "20241222", "20241228", "20241229"
]

base_path = Path(r"C:\Users\Owner\Desktop\Project\Web_Crawler\2024")

# 欄位名稱
cols = ['TimeStamp', 'GantryID', 'Direction', 'VehicleType', 'Volume']
target_ids = ['05F0001N', '05F0055N', '05F0287N']

count_processed = 0
count_skipped = 0

for date in dates:
    date_path = base_path / date
    if not date_path.exists():
        print(f"資料夾不存在，跳過: {date_path}")
        continue
    
    for hour in range(24):
        hour_str = f"{hour:02d}"
        hour_path = date_path / hour_str
        if not hour_path.exists():
            print(f"小時資料夾不存在，跳過: {hour_path}")
            continue
        
        csv_files = list(hour_path.glob("TDCS_M03A_*.csv"))
        if not csv_files:
            print(f"{hour_path} 找不到 csv 檔，跳過")
            continue
        
        for csv_file in csv_files:
            try:
                # 先讀檔檢查欄位
                df_check = pd.read_csv(csv_file, nrows=1)
                # 判斷欄位是不是已是彙整過的結構，跳過
                expected_cols_after = ['GantryID', 'Direction', 'Volume']
                if list(df_check.columns) == expected_cols_after:
                    print(f"已處理過，跳過: {csv_file}")
                    count_skipped += 1
                    continue
                
                # 沒跳過才正式讀取全部資料
                df = pd.read_csv(csv_file, header=None, names=cols)
                northbound_cars = df[(df['Direction'] == 'N') & (df['GantryID'].isin(target_ids))]
                Gantry_Volume = northbound_cars.groupby('GantryID').agg({
                    'Volume': 'sum',
                    'Direction': 'first'
                }).reset_index()
                Gantry_Volume = Gantry_Volume[['GantryID', 'Direction', 'Volume']]
                Gantry_Volume.to_csv(csv_file, index=False)
                print(f"處理完成: {csv_file}")
                count_processed += 1

            except Exception as e:
                print(f"處理失敗: {csv_file}，原因: {e}")

print(f"總共完成清洗檔案數: {count_processed}")
print(f"總共跳過已處理檔案數: {count_skipped}")