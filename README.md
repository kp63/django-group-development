# bluebird

## フォルダ構成
### プロジェクトルート
- `bluebird/` → プロジェクトフォルダ
- `core/` → 共通HTML&CSS部分の置き場所
    - `templates/` → 共通HTML
    - `static/` → 共通CSS&JS

- `threads/` → 掲示板機能
- `tweets/` → つぶやき機能
- `votes/` → 投票機能
- `askbox/` → 匿名質問箱機能
- `accounts/` → アカウント機能

### 各app内構成
- `<app名>/migrations/` → マイグレーションファイルの置き場所

- `<app名>/static/<app名>/` → 静的ファイル置き場 (CSS, JS, 画像等)
- `<app名>/templates/<app名>/` → Djangoテンプレート置き場 (HTML)

## コマンド集
### サーバー起動（スマート）
```sh
./dev
```
※venvの有効化、必要パッケージのインストール、データベースの初期化、マイグレーション、サーバー起動をすべて行うスクリプト

### サーバー起動（手動）
```sh
python manage.py runserver
```

### マイグレーション
models.pyに変更を加えた時はこのコマンドを実行する
```sh
python manage.py makemigrations
python manage.py migrate
```

---

### 初期化スクリプト
```sh
# ソースコードをダウンロード
git clone https://gogs.illustup.com/django/bluebird.git

# bluebirdフォルダに移動
cd bluebird

# venvの設定
python -m venv .venv --prompt bluebird
# Tips: ここで作成される.venvフォルダはGitコミットに含まれない
# (.gitignore内に記載されてるから)

# venvを有効化
. .venv\Scripts\activate

# 必要ライブラリのインストール
pip install -r requirements.txt
```
