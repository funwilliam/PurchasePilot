# 設定編碼為UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
Write-Host "已設定編碼為UTF8"

# 檢查是否以管理員身份運行
If (-Not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]"Administrator")) {
    Write-Host "以管理員身份重新運行此腳本..."
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    Exit
}

# 添加防火牆規則的函數
function Add-FirewallRule {
    param (
        [string]$ruleName,
        [int]$port,
        [string]$protocol
    )
    try {
        # 檢查防火牆規則是否已存在
        $ruleExists = netsh advfirewall firewall show rule name=$ruleName | Select-String "No rules match the specified criteria"
        if ($ruleExists) {
            netsh advfirewall firewall add rule name=$ruleName protocol=$protocol dir=in localport=$port action=allow
            Write-Host "防火牆規則已添加: $ruleName (Port: $port, Protocol: $protocol)"
        } else {
            Write-Host "防火牆規則已存在: $ruleName"
        }
    }
    catch {
        Write-Host "錯誤：無法添加防火牆規則 $ruleName (Port: $port, Protocol: $protocol)。請確保你有適當的權限。"
        pause
        exit
    }
}

# 定義刪除防火牆規則的函數
function Remove-FirewallRule {
    param (
        [string]$ruleName
    )
    try {
        # 檢查防火牆規則是否存在
        $ruleExists = netsh advfirewall firewall show rule name=$ruleName | Select-String "No rules match the specified criteria"
        if (-not $ruleExists) {
            netsh advfirewall firewall delete rule name=$ruleName
            Write-Host "防火牆規則已刪除: $ruleName"
        } else {
            Write-Host "防火牆規則不存在: $ruleName"
        }
    }
    catch {
        Write-Host "錯誤：無法刪除防火牆規則 $ruleName。請確保你有適當的權限。"
    }
}

# 獲取腳本所在目錄
$scriptPath = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent

# 導航到腳本所在目錄
Set-Location -Path $scriptPath
Write-Host "導航到腳本所在目錄：$scriptPath"

# 進入虛擬環境
Write-Host "進入虛擬環境..."
& .\venv\Scripts\Activate.ps1
Write-Host "虛擬環境已激活"

# 檢查伺服器是否正在運行，執行重啟
$pidFile = "$scriptPath\server.pid"
if (Test-Path $pidFile) {
    $processId = Get-Content $pidFile
    $existingProc = Get-Process -Id $processId -ErrorAction SilentlyContinue
    if ($existingProc) {
        Write-Host "伺服器已在運行，正在嘗試關閉..."
        Stop-Process -Id $processId -Force
        Remove-Item $pidFile -Force
    }
}

# 設置運行主機和端口
$serverHost  = "0.0.0.0"
$Port = "3636"
$Threads = "8"
$wsgiFactoryFunc = "run:waitress_entrypoint"

# 啟動伺服器
Write-Host "啟動伺服器..."
$process = Start-Process "waitress-serve" -ArgumentList "--host=$serverHost --port=$Port --threads=$Threads --call $wsgiFactoryFunc" -WindowStyle Hidden -PassThru
Set-Content -Path $pidFile -Value $process.Id -Encoding UTF8
Write-Host "伺服器已在背景運行，埠口: $Port，PID: $($process.Id)"

# 添加防火牆規則: 開放http, https port
# Write-Host "正在添加防火牆規則..."
# Add-FirewallRule -ruleName "AllowPurchasePilotHTTP" -port 80 -protocol "TCP"
# Add-FirewallRule -ruleName "AllowPurchasePilotHTTPS" -port 443 -protocol "TCP"
# Write-Host "已添加防火牆規則: AllowPurchasePilotHTTP, AllowPurchasePilotHTTPS"

Pause
