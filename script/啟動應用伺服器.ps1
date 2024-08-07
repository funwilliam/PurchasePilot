# 目錄導航
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
            Write-Host "警告: 雖然檔案 server.pid 存在，但該 PID 不在執行列表。" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "警告: 雖然檔案 server.pid 存在，但該 PID 不在執行列表。詳細錯誤信息：$_" -ForegroundColor Yellow
    }
}

# 進入虛擬環境
Write-Host "進入虛擬環境..."
& .\venv\Scripts\Activate.ps1
Write-Host "虛擬環境已啟用"

# 設置運行主機和端口
$serverHost  = "127.0.0.1"
$port = "3636"
$threadQuantity = "8"
$wsgiFactoryFunc = "run:waitress_entrypoint"
$URL = "http://$($serverHost):$($port)"

# 啟動伺服器
if ($isRunning) {
    Write-Host "正在重新啟動伺服器..."
}
else {
    Write-Host "正在啟動伺服器..."
}
# $process = Start-Process "waitress-serve" -WindowStyle Hidden -PassThru -ArgumentList "--host=$serverHost --port=$port --threads=$threadQuantity --call $wsgiFactoryFunc"
$process = Start-Process "python" -WindowStyle Hidden -PassThru -ArgumentList "-m waitress --host=$serverHost --port=$port --call $wsgiFactoryFunc"
Set-Content -Path $pidFile -Value $process.Id -Encoding UTF8
$URL | Set-Clipboard
Write-Host "伺服器已在背景運行，PID: $($process.Id)" -ForegroundColor Green
Write-Host "$($URL) ->已複製到剪貼版"

# # 添加防火牆規則: 開放http, https port
# Write-Host "正在添加防火牆規則..."
# Add-FirewallRule -ruleName "AllowPurchasePilotHTTP" -port 80 -protocol "TCP"
# Add-FirewallRule -ruleName "AllowPurchasePilotHTTPS" -port 443 -protocol "TCP"

Pause
