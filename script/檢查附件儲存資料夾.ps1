# 目錄導航
$scriptPath = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$projectRootPath = Split-Path -Path $scriptPath -Parent

# 載入模組
Set-Location -Path $scriptPath
Import-Module -Name .\UserDefinedToolkit

# 切換到專案根目錄
Set-Location -Path $projectRootPath

# 載入 .env 文件並取得環境變數
$envFilePath = ".\.env"
$baseFolder = ""

if (Test-Path $envFilePath) {
    $envContent = Get-Content $envFilePath -Encoding UTF8 | ForEach-Object {
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

Pause