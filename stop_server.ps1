# 設定編碼為UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
Write-Host "已設定編碼為UTF8"

# 獲取腳本所在目錄
$scriptPath = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent

# 導航到腳本所在目錄
Set-Location -Path $scriptPath
Write-Host "導航到腳本所在目錄：$scriptPath"

# 檢查是否以管理員身份運行
If (-Not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "以管理員身份重新運行此腳本..."
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    Exit
}

# 停止特定 Python 應用
if (Test-Path "server.pid") {
    $processId = Get-Content -Path "server.pid"
    if ($processId) {
        Write-Host "停止 Python 應用，進程ID：$processId"
        Stop-Process -Id $processId -Force
        Remove-Item -Path "server.pid"
        Write-Host "Python 應用已停止"
    } else {
        Write-Host "未找到有效的進程ID"
    }
} else {
    Write-Host "未找到server.pid文件"
}

# 刪除防火牆規則
Write-Host "刪除防火牆規則..."
netsh advfirewall firewall delete rule name="AllowPurchasePilotHTTP"
netsh advfirewall firewall delete rule name="AllowPurchasePilotHTTPS"
Write-Host "防火牆規則已刪除"
