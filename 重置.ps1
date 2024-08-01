# 設置 PowerShell 輸出編碼為 UTF-8
$OutputEncoding = [System.Text.Encoding]::UTF8

# 設置控制台代碼頁為 UTF-8
chcp 65001

# 獲取腳本所在目錄
$scriptPath = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent

# 導航到腳本所在目錄
Set-Location -Path $scriptPath

Pause

# 等待虛擬環境關閉
Start-Sleep -Seconds 2

# 刪除虛擬環境目錄
$venvPath = Join-Path -Path $scriptPath -ChildPath 'venv'
if (Test-Path -Path $venvPath) {
    Write-Host "刪除虛擬環境目錄..."
    Remove-Item -Recurse -Force $venvPath
    Write-Host "虛擬環境已刪除。"
} else {
    Write-Host "虛擬環境目錄不存在。"
}

Pause

# 刪除專案根目錄的 instance 和 migrations 資料夾
$instancePath = Join-Path -Path $scriptPath -ChildPath 'instance'
if (Test-Path -Path $instancePath) {
    Write-Host "刪除 instance 目錄..."
    Remove-Item -Recurse -Force $instancePath
    Write-Host "instance 目錄已刪除。"
} else {
    Write-Host "instance 目錄不存在。"
}

$migrationsPath = Join-Path -Path $scriptPath -ChildPath 'migrations'
if (Test-Path -Path $migrationsPath) {
    Write-Host "刪除 migrations 目錄..."
    Remove-Item -Recurse -Force $migrationsPath
    Write-Host "migrations 目錄已刪除。"
} else {
    Write-Host "migrations 目錄不存在。"
}

Pause

# 刪除整個專案所有 __pycache__ 資料夾
Write-Host "刪除所有 __pycache__ 目錄..."
Get-ChildItem -Path $scriptPath -Recurse -Filter '__pycache__' | Remove-Item -Recurse -Force
Write-Host "所有 __pycache__ 目錄已刪除。"

Pause

Write-Host "清理完成。"
