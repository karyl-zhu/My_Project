import os
import pandas as pd

root_folder = os.path.join(os.getcwd(), 'Web_Crawler', '2025')
output_root = os.path.join(os.getcwd(), 'data_clean', '2025')

processed_count = 0  # 計數成功處理的檔案數

for dirpath, dirnames, filenames in os.walk(root_folder):
    relative_path = os.path.relpath(dirpath, root_folder)
    parts = relative_path.split(os.sep)
    
    if len(parts) == 2:
        output_folder = os.path.join(output_root, parts[0], parts[1])
        os.makedirs(output_folder, exist_ok=True) 

        for file in filenames:
            if file.endswith('.csv'):
                file_path = os.path.join(dirpath, file)
                try:
                    df = pd.read_csv(file_path, header=None)
                    df.columns = ['TimeStamp', 'GantryFrom', 'GantryTo', 'VehicleType', 'Speed', 'Volume']
                    df[['Date', 'Time']] = df['TimeStamp'].str.split(' ', expand=True)
                    df = df[['Date', 'Time', 'TimeStamp', 'GantryFrom', 'GantryTo', 'VehicleType', 'Speed', 'Volume']]
                    
                    new_file_path = os.path.join(output_folder, file)
                    df.to_csv(new_file_path, index=False)
                    
                    processed_count += 1
                    print(f"成功處理檔案: {file_path}")
                except Exception as e:
                    print(f"處理檔案失敗: {file_path}")
                    print(f"錯誤訊息: {e}")

print(f"\n資料清洗完成！共計處理 {processed_count} 個 CSV 檔案。")
