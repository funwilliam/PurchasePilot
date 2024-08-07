# 目錄導航
$scriptPath = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$projectRootPath = Split-Path -Path $scriptPath -Parent

# 載入模組
Set-Location -Path $scriptPath
Import-Module -Name .\UserDefinedToolkit

# 切換到專案根目錄
Set-Location -Path $projectRootPath

# 刪除虛擬環境目錄
$venvPath = Join-Path -Path $projectRootPath -ChildPath 'venv'
if (Test-Path -Path $venvPath) {
    Write-Host "刪除虛擬環境目錄..."
    Remove-Item -Recurse -Force $venvPath
    Write-Host "虛擬環境已刪除。"
} else {
    Write-Host "虛擬環境目錄不存在。"
}

Pause

# 刪除專案根目錄的 instance 和 migrations 資料夾
$instancePath = Join-Path -Path $projectRootPath -ChildPath 'instance'
if (Test-Path -Path $instancePath) {
    Write-Host "刪除 instance 目錄..."
    Remove-Item -Recurse -Force $instancePath
    Write-Host "instance 目錄已刪除。"
} else {
    Write-Host "instance 目錄不存在。"
}

$migrationsPath = Join-Path -Path $projectRootPath -ChildPath 'migrations'
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
Get-ChildItem -Path $projectRootPath -Recurse -Filter '__pycache__' | Remove-Item -Recurse -Force
Write-Host "所有 __pycache__ 目錄已刪除。"

Pause

Write-Host "清理完成。"
