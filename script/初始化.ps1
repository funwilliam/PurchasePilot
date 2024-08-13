# 目錄導航
$scriptPath = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$projectRootPath = Split-Path -Path $scriptPath -Parent

# 載入模組
Set-Location -Path $scriptPath
Import-Module -Name .\UserDefinedToolkit

# 切換到專案根目錄
Set-Location -Path $projectRootPath

# 檢查虛擬環境是否已存在
if (Test-Path -Path ".\venv") {
    Write-Host "虛擬環境已存在，跳過建立步驟。"
} else {
    # 建立虛擬環境
    Write-Host "建立虛擬環境..."
    python -m venv venv
}

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

# 確認 log 資料夾是否已建立
if (Test-Path ".\log") {
    Write-Output "log 資料夾已存在。"
} else {
    Write-Output "log 建立資料夾建立。"
    New-Item -ItemType Directory -Path ".\log"
}

# 載入 .env 文件並取得環境變數
$envFilePath = ".\.env"
$baseFolder = ""

if (Test-Path $envFilePath) {
    $envContent = Get-Content $envFilePath | ForEach-Object {
        $_.Trim() | Where-Object { $_ -and $_ -notmatch "^#.*" } | ForEach-Object {
            $pair = $_ -split '=', 2
            $name = $pair[0].Trim()
            $value = $pair[1].Trim()
            if ($name -eq "FILES_STORAGE_FOLDER") {
                $baseFolder = $value
            }
        }
    }

    if (-not $baseFolder) {
        Write-Output "FILES_STORAGE_FOLDER 環境變數未找到或未設置。"
        exit
    }
} else {
    Write-Output "找不到 .env 文件。"
    exit
}

Write-Output "FILES_STORAGE_FOLDER 的值為：$baseFolder"

# 定義子資料夾名稱
$subFolders = @(
    "報價單",
    "規格圖",
    "未使用",
    "其他文件",
    "計畫書"
)

# 確認每個資料夾是否存在及是否為空
foreach ($subFolder in $subFolders) {
    $folder = Join-Path -Path $baseFolder -ChildPath $subFolder
    if (Test-Path $folder) {
        $files = Get-ChildItem -Path $folder
        if ($files.Count -eq 0) {
            Write-Output "資料夾 '$folder' 存在且為空。"
        }
        else {
            Write-Output "資料夾 '$folder' 存在但不是空的。"
        }
    }
    else {
        Write-Output "資料夾 '$folder' 不存在。"
    }
}

Write-Host "所有操作已完成。"

Pause
