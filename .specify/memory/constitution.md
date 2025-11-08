<!--
  Sync Impact Report: Constitution v1.0.0
  - Version: None → 1.0.0 (Initial establishment)
  - Added sections: 7 core principles, 4 sections (Guidelines, Metadata, Governance)
  - Ratified: 2025-11-08
  - Templates updated: None (baseline establishment)
-->

# ynym Portal Backend Constitution

プロジェクトの開発原則とガイドラインを定義する宣言書。すべてのチームメンバーはこの憲法に従って開発を進める。

## Core Principles

### I. 非同期優先 (Async-First)

すべての I/O 操作は非同期で実装する MUST。FastAPI、asyncpg、SQLModel の非同期機能を活用し、ブロッキング操作を徹底的に排除する。非同期コンテキストの使用は必須。パフォーマンスと拡張性を確保する。

### II. 型安全性の厳密実行 (Strict Type Safety)

Python 3.12+ の型ヒント機能を 100%活用する MUST。mypy の strict mode を必須とし、すべてのコードが型チェックを通過する MUST。型ヒント無しのコードは許可しない。IDE による型補完を最大活用。

### III. テスト駆動開発 (Test-Driven Development)

機能実装の前にテストコードを作成する TDD を厳密に実施する MUST。ユニットテスト・統合テスト・E2E テストの 3 層構造を採用。pytest を用いた包括的なテスト自動化。カバレッジ目標: 80% 以上。

### IV. レイヤー分離と責任の明確化 (Layered Architecture)

クリーンアーキテクチャの原則に従い、以下の 4 層に厳密に分離：

1. **API 層** (`app/api/endpoints/`) - HTTP リクエスト・レスポンス処理のみ
2. **スキーマ層** (`app/schemas/`) - Pydantic による入出力検証
3. **ビジネスロジック層** (`app/services/`) - コア業務ロジック
4. **データ層** (`app/models/`, `app/database.py`) - DB アクセス

層間の依存性は単方向（上位 → 下位のみ）。横方向の参照・跨ぎ参照は禁止。

### V. コード品質の自動化 (Automated Code Quality)

ruff (linting)・black (formatting)・mypy (type checking) による自動化を MUST。コード品質ゲートを手動レビュー前に実施。すべての開発ツールは `pyproject.toml` で集中管理。

### VI. ドキュメントは実装と同時進行 (Documentation as Code)

すべてのモジュール・クラス・関数に日本語の docstring を MUST とする。Swagger UI による自動 API ドキュメント生成。MkDocs による設計書・セットアップガイド・テスト方法論の整備。ドキュメントと実装の乖離は許可しない。

### VII. 明示的エラーハンドリング (Explicit Error Handling)

カスタム例外クラスを定義し、すべてのエラーを明示的に処理する MUST。例外クラス: `ApplicationException`, `ValidationException`, `NotFoundException`, `AuthenticationException`, `AuthorizationException`。スタックトレース・エラーメッセージの構造化を実装。

## Development Guidelines

### ディレクトリ構造と命名規則

- ディレクトリ名: 小文字、スネークケース (e.g., `app/security/`, `app/utils/`)
- ファイル名: 小文字、スネークケース (e.g., `user_service.py`, `jwt.py`)
- クラス名: PascalCase (e.g., `UserService`, `TodoModel`)
- 関数名: snake_case (e.g., `create_user()`, `verify_token()`)
- 定数: UPPER_SNAKE_CASE (e.g., `DEFAULT_TIMEOUT`, `MAX_RETRY_COUNT`)
- プライベート関数/変数: 先頭にアンダースコア (e.g., `_internal_helper()`)

### API レスポンス形式（統一）

すべての API レスポンスは以下の統一フォーマットに従う MUST：

**成功レスポンス (2xx)**:

```json
{
  "data": {
    /* レスポンスデータ */
  },
  "message": "操作名が成功しました"
}
```

**エラーレスポンス (4xx, 5xx)**:

```json
{
  "detail": "エラーメッセージ",
  "status_code": 400,
  "error_type": "ValidationException"
}
```

### JWT 認証と認可

- JWT シークレットキーは環境変数 `JWT_SECRET_KEY` で管理 MUST
- 本番環境では強力なランダムキーを設定 MUST
- トークン有効期限: 環境変数 `JWT_EXPIRATION_HOURS` で制御（デフォルト 24 時間）
- 認証が必要なエンドポイントは `Authorization: Bearer <token>` ヘッダーで実装
- トークン検証エラー時は `AuthenticationException` (401) を返す MUST

### 環境変数管理

- `.env.example` にすべての必須環境変数を記載する MUST
- `.env` は `.gitignore` に含め、本番環境では環境変数で設定
- 環境変数は `app/config.py` の `Settings` クラスで集中管理
- 環境ごとに異なる値（DB 接続情報、JWT シークレット等）は環境変数で切り替え

**必須環境変数**:

- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
- `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_EXPIRATION_HOURS`
- `ENVIRONMENT` (development / staging / production)
- `LOG_LEVEL` (DEBUG / INFO / WARNING / ERROR)

### ロギング戦略

- 標準ライブラリ `logging` モジュール使用 MUST
- ログレベル: DEBUG (開発)、INFO (本番アクセス記録)、WARNING (予期しない状況)、ERROR (エラー)
- 本番環境では JSON フォーマット化を検討
- 機密情報（パスワード、トークン等）をログに出力することは厳禁

### データベース設計

- PostgreSQL 12+ を使用 MUST
- SQLModel で モデルを定義（SQLAlchemy ORM + Pydantic スキーマ統合）
- asyncpg で非同期接続を実装
- マイグレーションツール（Alembic）は将来的に導入予定。現在は手動管理。
- すべてのテーブルに `created_at`, `updated_at` タイムスタンプを MUST

### テスト戦略

**ユニットテスト** (`tests/unit/`):

- サービス層・ユーティリティ関数のテスト
- 外部依存性はモック化
- テスト実行: `pytest tests/unit/`

**統合テスト** (`tests/integration/`):

- エンドポイント・データベース連携のテスト
- 実テスト DB または テストデータベースコンテナ使用
- テスト実行: `pytest tests/integration/`

**テスト実行時の環境**:

- `pytest.ini` で自動モード設定: `asyncio_mode = "auto"`
- テスト用 fixture は `tests/conftest.py` で管理

### セキュリティ要件

- パスワードハッシング: bcrypt (passlib ライブラリ) MUST
- JWT 署名アルゴリズム: HS256 (環境変数で制御可能)
- CORS: 開発時は `*`、本番環境では明示的にホワイトリスト化 MUST
- 本番環境では HTTPS/TLS を MUST
- 入力値は Pydantic スキーマで検証（二重検証は不要）

## Project Metadata

### 技術スタック

- **言語**: Python 3.12+
- **Web フレームワーク**: FastAPI
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **データベース**: PostgreSQL 12+
- **非同期ドライバ**: asyncpg
- **パッケージ管理**: uv
- **認証**: JWT (python-jose)
- **パスワード管理**: bcrypt (passlib)
- **テスト**: pytest, pytest-asyncio
- **コード品質**: ruff (linting), mypy (type checking)
- **ドキュメント**: MkDocs + Material テーマ
- **設定管理**: Pydantic Settings

### ファイル構成

```
ynym-portal-backend/
├── app/                    # アプリケーション本体
│   ├── api/endpoints/      # API エンドポイント
│   ├── models/             # SQLModel DB モデル
│   ├── schemas/            # Pydantic スキーマ
│   ├── services/           # ビジネスロジック
│   ├── security/           # JWT・パスワード処理
│   ├── utils/              # 例外・ログ設定
│   ├── config.py           # 環境変数管理
│   ├── database.py         # DB 接続管理
│   └── main.py             # FastAPI アプリ起動
├── tests/                  # テストコード
│   ├── unit/               # ユニットテスト
│   ├── integration/        # 統合テスト
│   └── conftest.py         # pytest 設定・fixture
├── docs/                   # MkDocs ドキュメント
│   ├── api/                # API 仕様書
│   ├── development/        # 開発ガイド
│   └── deployment/         # デプロイメントガイド
├── .env.example            # 環境変数テンプレート
├── .gitignore              # Git 除外設定
├── .specify/               # プロジェクト管理メタデータ
├── pyproject.toml          # uv パッケージ設定
├── mkdocs.yml              # MkDocs 設定
└── README.md               # プロジェクト概要
```

### リリースサイクルと版管理

- **バージョニング**: セマンティックバージョニング (MAJOR.MINOR.PATCH)
  - MAJOR: API 破壊的変更（モデル削除、スキーマ大幅変更）
  - MINOR: 新機能追加（エンドポイント追加、モデル拡張）
  - PATCH: バグ修正、ドキュメント更新、内部リファクタリング
- 各リリースは git tag で記録: `v1.2.3`

## Governance

### 憲法の遵守

このドキュメントはプロジェクトの法的効力を持つ開発原則である。すべての PR・コミット・リリースはこれらの原則を遵守する MUST。

### 原則違反時の対応

1. コードレビュー時に原則違反を検出した場合は、修正を要求する。
2. 自動ツール（mypy, ruff）で検出可能な違反は、マージ前に修正する MUST。
3. 意図的に原則を逸脱する場合は、以下を必須とする：
   - 逸脱の理由を明示的に書き残す（コメント、PR 説明）
   - チームメンバー全員の同意を得る
   - 今後の改善計画を記載する

### 憲法の改正

新しい原則を追加・既存原則を修正する場合：

1. PR で提案し、チームメンバーから 1 件以上の承認を得る
2. 改正理由・影響範囲を明確に説明する
3. 本ドキュメント（`.specify/memory/constitution.md`）と関連テンプレートを更新する
4. git commit message: `docs: amend constitution to vX.Y.Z (principle: change description)`

### 開発ガイドの参照先

実装時の詳細ガイドは以下を参照：

- `docs/development/setup.md` - 開発環境セットアップ
- `docs/development/architecture.md` - アーキテクチャ詳細
- `docs/development/testing.md` - テスト実行方法
- `docs/deployment/production.md` - 本番デプロイメント

---

**Version**: 1.0.0 | **Ratified**: 2025-11-08 | **Last Amended**: 2025-11-08
