import pandas as pd
import glob
import os

data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'raw')

file_path = glob.glob(os.path.join(data_path, 'health_3_*.xlsx'))[0]
df = pd.read_excel(file_path, header=None)

print("Смотрим строки с 7 по 23 и столбцы с 0 по 6:")
for i in range(7, 23):
    row_data = df.iloc[i, 0:7].values
    print(f"Строка {i}: {row_data}")
