import pyodbc
import pandas as pd
from run import create_app, db
from app import 供應商, 專案

data_set = {
    'suppliers': [],
    'projects': [],
    'units': [],
    'currencies': [],
    'material_categories': []
}

# 連接到 Microsoft Access 資料庫
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=instance\工程部-請購表單.accdb;'
)
conn = pyodbc.connect(conn_str)

# SQL 查詢，讀取資料表
sql_query = 'SELECT 供應商代號, 供應商簡稱, 營業項目, 供應商全名 FROM 廠商資料'

# 使用 pandas 讀取資料
df = pd.read_sql(sql_query, conn)

# 迭代每一列，取得特定欄位的資料
for index, row in df.iterrows():
    供應商代號 = row['供應商代號']
    供應商簡稱 = row['供應商簡稱']
    營業項目 = row['營業項目']
    供應商全名 = row['供應商全名']

    data_set['suppliers'].append(
        供應商(供應商編號=供應商代號, 簡稱=供應商簡稱, 全名=供應商全名, 營業項目=營業項目)
    )

# SQL 查詢，讀取資料表
sql_query = 'SELECT 正式專案名稱, 年份, 其他名稱參考 FROM 專案列表'

# 使用 pandas 讀取資料
df = pd.read_sql(sql_query, conn)

# 迭代每一列，取得特定欄位的資料
for index, row in df.iterrows():
    正式專案名稱 = row['正式專案名稱']
    年份 = row['年份']
    其他名稱參考 = row['其他名稱參考']

    data_set['projects'].append(
        專案(專案名稱=正式專案名稱, 啟動年份=年份, 備註=其他名稱參考)
    )

# 關閉連接
conn.close()

# 使用 pandas 讀取資料
df = pd.read_csv('instance\currencies.csv', encoding='utf-8')

# 迭代每一列，取得特定欄位的資料
for index, row in df.iterrows():
    幣別代號 = row['幣別代號']
    幣別名稱 = row['幣別名稱']
    維運組織 = row['維運組織']

    data_set['currencies'].append(
        專案(代號=幣別代號, 名稱=幣別名稱, 維運組織=維運組織)
    )

app = create_app()
with app.app_context():
    for key in data_set:
        db.session.bulk_save_objects(data_set[key])
    db.session.commit()
