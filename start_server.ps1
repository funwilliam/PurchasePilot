# 設定編碼為UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
Write-Host "已設定編碼為UTF8"

# 獲取腳本所在目錄
$scriptPath = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent

# 導航到腳本所在目錄
Set-Location -Path $scriptPath
Write-Host "導航到腳本所在目錄：$scriptPath"

# 進入虛擬環境
# Write-Host "進入虛擬環境..."
# & .\venv\Scripts\Activate.ps1
# Write-Host "虛擬環境已激活"

# 檢查是否以管理員身份運行
If (-Not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "以管理員身份重新運行此腳本..."
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    Exit
}

# 添加防火牆規則
Write-Host "添加防火牆規則..."
netsh advfirewall firewall add rule name="AllowPurchasePilotHTTP" protocol=TCP dir=in localport=80 action=allow
netsh advfirewall firewall add rule name="AllowPurchasePilotHTTPS" protocol=TCP dir=in localport=443 action=allow
Write-Host "防火牆規則已添加"

# 設置Python腳本和端口
$PythonExePath = ".\venv\Scripts\python.exe"  # 更新為你的Python執行檔路徑
$ScriptPath = ".\run.py"  # 更新為你的Python腳本路徑
$Port = 80

# 以管理員身份運行Python腳本
Write-Host "以管理員身份運行Python腳本..."
$process = Start-Process -FilePath $PythonExePath -ArgumentList "$ScriptPath --port $Port" -PassThru
$processId = $process.Id
Set-Content -Path "server.pid" -Value $processId
Write-Host "Python應用已啟動在端口 $Port，進程ID：$processId"
