"""Pydantic Settings を使用したアプリケーション設定."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """環境変数から読み込まれたアプリケーション設定."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_ignore_empty=True
    )

    # データベース接続設定
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    @property
    def database_url(self) -> str:
        """個別の要素からデータベース URL を組み立てる."""
        return (
            f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # JWT 認証設定
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_MINUTES: int

    # Google OAuth2 設定
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    # URL 設定
    FRONTEND_URL: str
    BACKEND_URL: str

    # CORS 設定（カンマ区切りで複数指定可能）
    ALLOWED_ORIGINS: str

    @property
    def cors_origins(self) -> list[str]:
        """カンマ区切りの文字列をリストに変換."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    # 環境設定
    ENVIRONMENT: str
    LOG_LEVEL: str


# グローバル設定インスタンス
settings = Settings()
