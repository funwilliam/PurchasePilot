# 設定編碼為UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$moduleName = 'UserDefinedToolkit'
Write-Host "模組 $($moduleName) 已設定編碼為UTF8" -ForegroundColor DarkGray

# 定義遞歸函數以停止進程及其子進程
function Stop-ProcessTree {
    param (
        [int]$ProcessId
    )

    # 跳過系統進程
    if ($ProcessId -eq 0 -or $ProcessId -eq 4) {
        Write-Host "跳過 PID=$($ProcessId)" -ForegroundColor DarkGray
        return
    }

    # 獲取當前進程信息
    try {
        $Process = Get-CimInstance Win32_Process -Filter "ProcessId = $ProcessId"
    }
    catch {
        Write-Host "無法獲取進程 PID: $($ProcessId) 的信息。詳細錯誤信息: $_" -ForegroundColor Red
        return
    }

    Write-Host "找到進程: $($Process.Name) (PID: $($ProcessId), Parent PID: $($Process.ParentProcessId))" -ForegroundColor DarkGray

    # 獲取子進程
    try {
        $ChildProcesses = @(Get-CimInstance Win32_Process | Where-Object { $_.ParentProcessId -eq $ProcessId })
    }
    catch {
        Write-Host "無法獲取子進程。詳細錯誤信息: $_" -ForegroundColor Red
        return
    }

    if ($ChildProcesses.Count -gt 0) {
        Write-Host "進程 PID: $($ProcessId) 有子進程: $($ChildProcesses | ForEach-Object { $_.ProcessId -join ', ' })" -ForegroundColor DarkGray
    }
    else {
        Write-Host "進程 PID: $($ProcessId) 沒有子進程" -ForegroundColor DarkGray
    }

    # 遞歸關閉子進程
    foreach ($ChildProcess in $ChildProcesses) {
        if ($ChildProcess.ProcessId -ne 0 -and $ChildProcess.ProcessId -ne 4) {
            Stop-ProcessTree -ProcessId $ChildProcess.ProcessId
        }
    }

    # 關閉當前進程
    try {
        Stop-Process -Id $ProcessId -Force
        Write-Host "成功: PID 為 $($ProcessId) 的處理程序已終止。" -ForegroundColor Green
    }
    catch {
        Write-Host "失敗: 無法停止 PID 為 $($ProcessId) 的處理程序。詳細錯誤信息: $($_.Exception.Message)" -ForegroundColor Red
    }
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
        $ruleExists = netsh advfirewall firewall show rule name=$($ruleName) | Select-String $ruleName
        if ($ruleExists) {
            Write-Host "防火牆規則已存在: $($ruleName)" -ForegroundColor Yellow
        }
		else {
			netsh advfirewall firewall add rule name=$($ruleName) protocol=$($protocol) dir=in localport=$($port) action=allow
            Write-Host "防火牆規則已添加: $($ruleName) (Port: $($port), Protocol: $($protocol))" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "錯誤：無法添加防火牆規則 $($ruleName) (Port: $($port), Protocol: $($protocol))。請確保你有適當的權限。" -ForegroundColor Red
    }
}

# 定義刪除防火牆規則的函數
function Remove-FirewallRule {
    param (
        [string]$ruleName
    )
    try {
        # 檢查防火牆規則是否存在
        $ruleExists = netsh advfirewall firewall show rule name=$($ruleName) | Select-String $ruleName
        if ($ruleExists) {
            netsh advfirewall firewall delete rule name=$($ruleName)
            Write-Host "防火牆規則已刪除: $($ruleName)" -ForegroundColor Green
        }
		else {
            Write-Host "防火牆規則不存在: $($ruleName)" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "錯誤：無法刪除防火牆規則 $($ruleName)。請確保你有適當的權限。" -ForegroundColor Red
    }
}
