# ynym Portal Backend

ynym portal 向けの FastAPI バックエンドシステム。

## 主な機能・特徴

- **FastAPI**: 高パフォーマンスな非同期 Web フレームワーク
- **SQLAlchemy 2.0**: モダンな非同期 ORM
- **PostgreSQL**: `psycopg` を利用した堅牢なリレーショナルデータベース接続
- **認証・認可**: JWT（トークンベース）および Google OAuth 認証
- **型安全性**: Pydantic v2 による厳格なリクエスト / レスポンスバリデーション
- **品質管理**: Ruff による高速な Lint / フォーマット
- **テスト**: pytest によるユニット・統合テスト
- **ドキュメント自動生成**: Swagger UI (`/docs`) および ReDoc (`/redoc`) による対話型 API ドキュメント

## 前提条件

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) パッケージマネージャー
- PostgreSQL 12+ (または Docker)

## クイックスタート

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd ynym-portal-backend
```

### 2. 依存パッケージのインストール

```bash
uv sync
```

### 3. 環境変数の設定

`.env.sample` を `.env` にコピーし、環境に合わせて設定を更新します。

```bash
cp .env.sample .env
```

主な環境変数:

- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`: PostgreSQL 接続設定
- `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_EXPIRE_MINUTES`: JWT 認証トークン設定
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`: Google OAuth 認証設定
- `FRONTEND_URL`, `BACKEND_URL`, `ALLOWED_ORIGINS`: CORS / 接続先 URL 設定
- `ENVIRONMENT`: 動作環境 (`development`, `production` など)
- `LOG_LEVEL`: ログレベル (`DEBUG`, `INFO`, `WARNING`, `ERROR`)

### 4. データベースのセットアップ

`migrations/` ディレクトリ内の SQL スクリプトを使用してテーブルの作成を行います。  
詳細は [migrations/README.md](migrations/README.md) を参照してください。

### 5. 開発サーバーの起動

```bash
uv run uvicorn app.main:app --reload
```

起動後、以下の URL にアクセスできます:

- API ルート: http://localhost:8000
- Swagger UI (対話型ドキュメント): http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker での実行

Docker および Docker Compose を使用してコンテナをビルド・起動できます。

```bash
# コンテナのビルド
docker compose build

# バックグラウンドで起動
docker compose up -d
```

## 開発・コード品質

### テストの実行

```bash
# すべてのテストを実行
uv run pytest

# ユニットテストのみ実行
uv run pytest -m unit

# 統合テストのみ実行
uv run pytest -m integration
```

### Lint & フォーマット

```bash
# Lint チェック
uv run ruff check app tests

# Lint 自動修正
uv run ruff check --fix app tests

# コードフォーマット
uv run ruff format app tests
```

### ドキュメント生成 (MkDocs)

```bash
uv run mkdocs serve
```

## プロジェクト構成

```
ynym-portal-backend/
├── app/                  # アプリケーションコード
│   ├── core/            # コア設定・DB 接続定義 (config.py, db.py)
│   ├── middleware/      # ミドルウェア (ロギング等)
│   ├── models/          # SQLAlchemy データモデル
│   ├── repositories/    # データアクセス層
│   ├── routers/         # API ルーター / エンドポイント
│   ├── schemas/         # Pydantic スキーマ (リクエスト/レスポンス)
│   ├── security/        # 認証・セキュリティ関連処理
│   ├── services/        # ビジネスロジック層
│   ├── utils/           # ユーティリティ・例外ハンドリング
│   └── main.py          # FastAPI アプリケーションのエントリポイント
├── docs/                # プロジェクトドキュメント (MkDocs)
├── migrations/          # データベースマイグレーション用 SQL
├── tests/               # テストコード
│   ├── unit/            # ユニットテスト
│   └── integration/     # 統合テスト
├── compose.yml          # Docker Compose 設定
├── Dockerfile           # Docker ビルド設定
├── pyproject.toml       # プロジェクト設定・依存関係定義
└── uv.lock              # 依存関係ロックファイル
```

## ライセンス

[ライセンス情報をここに記載]
