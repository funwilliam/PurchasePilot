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

# 停止運行伺服器
$pidFile = "$scriptPath\server.pid"
if (Test-Path $pidFile) {
    $processId = Get-Content $pidFile
    $existingProc = Get-Process -Id $processId -ErrorAction SilentlyContinue
    if ($existingProc) {
        Write-Host "正在關閉伺服器..."
        Stop-Process -Id $processId -Force
        Remove-Item $pidFile -Force
        Write-Host "伺服器已關閉"
		
		# 刪除防火牆規則
		# Write-Host "正在刪除防火牆規則..."
		# Remove-FirewallRule -ruleName "AllowPurchasePilotHTTP"
		# Remove-FirewallRule -ruleName "AllowPurchasePilotHTTPS"
		# Write-Host "已添加防火牆規則: AllowPurchasePilotHTTP, AllowPurchasePilotHTTPS"
    } else {
        Write-Host "沒有找到正在運行的伺服器。"
    }
} else {
    Write-Host "沒有找到 PID 文件，伺服器可能未在運行。"
}

Pause