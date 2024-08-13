from typing import Literal, List, Dict
import pandas as pd
from run import create_app, db
from app import 供應商, 單位, 幣別, 員工, 專案, 捷拓廠區, 請購類型, 物料類別, 物料


col_keys = ['供應商', '單位', '幣別', '員工', '專案', '捷拓廠區', '請購類型', '物料類別', '物料']
data_set: Dict[Literal['供應商', '單位', '幣別', '員工', '專案', '捷拓廠區', '請購類型', '物料類別', '物料'], List] = {key: [] for key in col_keys}

a = data_set['供應商']


# 取得供應商CSV檔資料
df = pd.read_csv('data\供應商.csv', encoding='utf-8', dtype={'供應商編號': str})
df = df.where(pd.notnull(df), None)
for index, row in df.iterrows():
    data_set['供應商'].append(
        供應商(
            供應商編號=row['供應商編號'],
            簡稱=row['簡稱'],
            全名=row['全名'],
            營業項目=row['營業項目']
        )
    )


# 取得單位CSV檔資料
df = pd.read_csv('data\單位.csv', encoding='utf-8')
df = df.where(pd.notnull(df), None)
for index, row in df.iterrows():
    data_set['單位'].append(
        單位(
            代碼=row['代碼'],
            中文含意=row['中文含意'],
            英文含意=row['英文含意']
        )
    )


# 取得幣別CSV檔資料
df = pd.read_csv('data\幣別.csv', encoding='utf-8')
df = df.where(pd.notnull(df), None)
for index, row in df.iterrows():
    data_set['幣別'].append(
        幣別(
            代號=row['代號'],
            名稱=row['名稱'],
            維運組織=row['維運組織']
        )
    )


# 取得員工CSV檔資料
df = pd.read_csv('data\員工.csv', encoding='utf-8')
df = df.where(pd.notnull(df), None)
for index, row in df.iterrows():
    data_set['員工'].append(
        員工(
            工號簡碼=row['工號簡碼'],
            工號全碼=row['工號全碼'],
            姓名=row['姓名'],
            信箱=row['信箱'],
            員工卡號=row['員工卡號']
        )
    )


# 取得專案CSV檔資料
df = pd.read_csv('data\專案.csv', encoding='utf-8')
df = df.where(pd.notnull(df), None)
for index, row in df.iterrows():
    data_set['專案'].append(
        專案(
            專案名稱=row['專案名稱'],
            啟動年份=row['啟動年份'],
            負責人工號簡碼=row['負責人工號簡碼'],
            備註=row['備註'],
        )
    )


# 取得捷拓廠區CSV檔資料
df = pd.read_csv('data\捷拓廠區.csv', encoding='utf-8', dtype={'地址碼': str})
df = df.where(pd.notnull(df), None)
for index, row in df.iterrows():
    data_set['捷拓廠區'].append(
        捷拓廠區(
            廠區名稱=row['廠區名稱'],
            地址碼=row['地址碼'],
            地址=row['地址']
        )
    )


# 取得請購類型CSV檔資料
df = pd.read_csv('data\請購類型.csv', encoding='utf-8')
df = df.where(pd.notnull(df), None)
for index, row in df.iterrows():
    data_set['請購類型'].append(
        請購類型(
            類型=row['類型']
        )
    )


# 取得物料類別CSV檔資料
df = pd.read_csv('data\物料類別.csv', encoding='utf-8')
df = df.where(pd.notnull(df), None)
for index, row in df.iterrows():
    data_set['物料類別'].append(
        物料類別(
            類別=row['類別']
        )
    )


# 取得物料CSV檔資料
df = pd.read_csv('data\物料.csv', encoding='utf-8')
df = df.where(pd.notnull(df), None)
for index, row in df.iterrows():
    data_set['物料'].append(
        物料(
            物料代號=row['物料代號'],
            供應商簡稱=row['供應商簡稱'],
            品名規格=row['品名規格'],
            單價=row['單價'],
            幣別=row['幣別'],
            單位=row['單位'],
            預設收貨廠區=row['預設收貨廠區'],
        )
    )

# # 連接到 Microsoft Access 資料庫
# conn_str = (
#     r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
#     r'DBQ=data\工程部-請購表單.accdb;'
# )
# import pyodbc
# conn = pyodbc.connect(conn_str)

# # SQL 查詢，讀取資料表
# sql_query = 'SELECT 供應商代號, 供應商簡稱, 營業項目, 供應商全名 FROM 廠商資料'

# # 使用 pandas 讀取資料
# df = pd.read_sql(sql_query, conn)

# # 迭代每一列，取得特定欄位的資料
# for index, row in df.iterrows():
#     供應商代號  = row['供應商代號']
#     供應商簡稱  = row['供應商簡稱']
#     營業項目    = row['營業項目']
#     供應商全名  = row['供應商全名']

#     data_set['供應商'].append(
#         供應商(供應商編號=供應商代號, 簡稱=供應商簡稱, 全名=供應商全名, 營業項目=營業項目)
#     )

# # 關閉連接
# conn.close()


app = create_app()
with app.app_context():
    for key in data_set:
        db.session.bulk_save_objects(data_set[key])
    db.session.commit()


# 試錯
# app = create_app()
# with app.app_context():
#     df = pd.read_csv('data\物料.csv', encoding='utf-8')
#     for index, row in df.iterrows():
        
#         tmp = 物料(
#             物料代號=row['物料代號'],
#             供應商簡稱=row['供應商簡稱'],
#             品名規格=row['品名規格'],
#             單價=row['單價'],
#             幣別=row['幣別'],
#             單位=row['單位'],
#             預設收貨廠區=row['預設收貨廠區'],
#         )
#         db.session.add(tmp)

#         if index % 50 == 0:
#             db.session.commit()