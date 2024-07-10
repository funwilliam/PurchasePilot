@echo off
REM 創建虛擬環境
python -m venv venv

REM 進入虛擬環境
call venv\Scripts\activate.bat

REM 初始化專案的import
python auto_imports.py

REM 安裝必要套件
pip install -r requirements.txt

REM 初始化資料庫
flask db init
flask db migrate -m "Initial migration."
flask db upgrade

pause

REM 輸入資料到資料庫內
python init_insert_data.py

echo 專案初始化完成
pause
