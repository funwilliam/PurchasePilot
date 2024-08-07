﻿# 目錄導航
$scriptPath = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$projectRootPath = Split-Path -Path $scriptPath -Parent

# 載入模組
Set-Location -Path $scriptPath
Import-Module -Name .\UserDefinedToolkit

# 檢查是否以管理員身份運行
If (-Not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]"Administrator")) {
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    Write-Host "以管理員身份重新運行此腳本，正在退出..." -ForegroundColor Green
	Exit
}
Write-Host "正以管理員身份運行此腳本中..." -ForegroundColor DarkGray

# 切換到專案根目錄
Set-Location -Path $projectRootPath

# 檢查伺服器是否正在運行，停止運行伺服器
$isRunning = $false
$pidFile = ".\log\server.pid"
if (Test-Path $pidFile) {
    $serverPid = Get-Content $pidFile
    try {
        $process = Get-Process -Id $serverPid -ErrorAction Stop
        if ($process) {
            Write-Host "伺服器主程序的PID: $($serverPid), 正在嘗試關閉..."
            try {
                Stop-ProcessTree -ProcessId $serverPid
                $isRunning = $true
                Remove-Item -Path $pidFile -Force
                Write-Host "伺服器主程序及其子進程已結束。" -ForegroundColor Green
            }
            catch {
                Write-Host "錯誤: 結束伺服器主程序及其子進程時發生錯誤。詳細錯誤信息：$_" -ForegroundColor Red
            }
        }
        else {
            Remove-Item -Path $pidFile -Force
            Write-Host "警告: 雖然檔案 server.pid 存在，但該 PID 不在執行列表，刪除 server.pid。" -ForegroundColor Yellow
        }
    }
    catch {
        Remove-Item -Path $pidFile -Force
        Write-Host "警告: 雖然檔案 server.pid 存在，但該 PID 不在執行列表，刪除 server.pid。" -ForegroundColor Yellow
    }
}
else {
    Write-Host "警告: 沒有找到 PID 文件，伺服器可能未在運行。" -ForegroundColor Yellow
}

# # 刪除防火牆規則
# if ($isRunning) {
# 	try {
# 		Write-Host "正在刪除防火牆規則..."
#         Remove-FirewallRule -ruleName "AllowPurchasePilotHTTP"
#         Remove-FirewallRule -ruleName "AllowPurchasePilotHTTPS"
# 	}
# 	catch {
# 		Write-Host "刪除防火牆規則時發生錯誤。" -ForegroundColor Red
# 	}
# }
# else {
# 	Write-Host "警告: 伺服器未運行or關閉時發生錯誤，因此未執行刪除防火牆規則: AllowPurchasePilotHTTP, AllowPurchasePilotHTTPS" -ForegroundColor Yellow
# }

Pause