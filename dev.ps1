$apps = ("core", "accounts", "threads", "tweets", "votes", "askbox", "contact")

function Check-PipRequirements {
    param (
        [string]$requirementsFile = "requirements.txt"
    )

    # インストール済みパッケージを一括取得
    $installedPackages = pip freeze | ForEach-Object {
        $parts = $_ -split "=="
        [PSCustomObject]@{
            Name = $parts[0]
            Version = $parts[1]
        }
    }

    # requirements.txtを確認
    $requirements = Get-Content -Path $requirementsFile
    $installNeeded = $false

    foreach ($line in $requirements) {
        if ($line -match "^([^=]+)==(.+)$") {
            $package = $matches[1]
            $requiredVersion = $matches[2]
            $installed = $installedPackages | Where-Object { $_.Name -eq $package }

            # パッケージが未インストールまたはバージョン不一致の場合はインストールが必要
            if (-not $installed -or $installed.Version -ne $requiredVersion) {
                $installNeeded = $true
                break
            }
        }
    }
    return $installNeeded
}


if (Test-Path .\.venv) {
    . .\.venv\Scripts\Activate.ps1
    Write-Host -ForegroundColor DarkGray "> venvを有効化しました (.venv)"
}

if (Check-PipRequirements) {
    Write-Host -ForegroundColor DarkGray "> 必要なパッケージをインストールします"
    pip install -r requirements.txt
} 

Write-Host -ForegroundColor DarkGray "> プロジェクトをチェックします"
python manage.py check
if ($LASTEXITCODE -ne 0) {
    Write-Host -ForegroundColor Red "! プロジェクトのチェックで問題が検出されました"
    exit 1
}

$argumentList = $args | ForEach-Object { $_.ToLower() }
$resetDatabase = $argumentList -contains "resetdb"

if ($resetDatabase) {
    Write-Host -ForegroundColor DarkGray "> データベースを初期化します"

    # 各アプリのmigrationsフォルダ内のマイグレーションファイルを削除
    foreach ($app in $apps) {
        $migrationsDir = ".\${app}\migrations"
        if (Test-Path $migrationsDir) {
            Get-ChildItem -Path $migrationsDir -Recurse -Include __pycache__ | Remove-Item -Recurse -Force
            Get-ChildItem -Path $migrationsDir | Where-Object { $_.Name -ne "__init__.py" } | Remove-Item -Force
        }
    }
}

Write-Host -ForegroundColor DarkGray "> モデルの変更を確認します"
python manage.py makemigrations
if ($LASTEXITCODE -ne 0) {
    Write-Host -ForegroundColor Red "! makemigrationsに失敗しました"
    exit 1
}

$changes = python manage.py showmigrations | Where-Object { $_ -match "^[ ]+\[ \]" }
if ($changes) {
    Write-Host -ForegroundColor DarkGray "> モデルの変更を適用します"
    python manage.py migrate
    if ($LASTEXITCODE -ne 0) {
        Write-Host -ForegroundColor Red "! migrateに失敗しました"
        exit 1
    }
}

if ($resetDatabase) {
    $response = Read-Host -Prompt "スーパーユーザーを作成しますか？ [y/N]"
    if ($response -eq "y") {
        Write-Host -ForegroundColor DarkGray "> スーパーユーザーを作成します"
        python manage.py createsuperuser
        if ($LASTEXITCODE -ne 0) {
            Write-Host -ForegroundColor Red "! スーパーユーザーの作成に失敗しました"
            exit 1
        }
    }
}

Write-Host -ForegroundColor DarkGray "> 開発サーバーを起動します"
python manage.py runserver
