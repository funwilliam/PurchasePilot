﻿$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001

Write-Host "已設定編碼為UTF8"
Pause

# 獲取腳本所在目錄
$scriptPath = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent

# 導航到腳本所在目錄
Set-Location -Path $scriptPath

# 顯示進度：導航到腳本所在目錄
Write-Host "導航到腳本所在目錄：$scriptPath"

# 建立虛擬環境
Write-Host "建立虛擬環境..."
python -m venv venv

# 進入虛擬環境
Write-Host "進入虛擬環境..."
& .\venv\Scripts\Activate.ps1

# 初始化專案的import
Write-Host "初始化專案的import..."
python .\app\helpers\auto_imports.py

Pause

# 安裝必要的套件
Write-Host "安裝必要的套件..."
pip install -r requirements.txt

# 生成 SECRET_KEY 並寫入 .env 文件
Write-Host "生成 SECRET_KEY 並寫入 .env 文件..."
python .\app\helpers\generate_secret_key.py

# 初始化資料庫
Write-Host "初始化資料庫..."
flask db init
Write-Host "進行資料庫遷移..."
flask db migrate -m "Initial migration."
Write-Host "升級資料庫..."
flask db upgrade

Pause

# 輸入資料到資料庫
Write-Host "輸入資料到資料庫..."
python seed_data.py

# 結束後退出虛擬環境
Write-Host "退出虛擬環境..."
deactivate

Write-Host "所有操作已完成。"

Pause