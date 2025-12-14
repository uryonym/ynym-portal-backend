"""Pydantic Settings を使用したアプリケーション設定."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """環境変数から読み込まれたアプリケーション設定."""

    # データベース
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "ynym_portal"
    db_user: str = "username"
    db_password: str = "password"

    # JWT
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30

    # Google認証
    google_client_id: str
    google_client_secret: str

    # URL
    backend_url: str = "http://localhost:8000"

    # 環境
    environment: str = "development"
    log_level: str = "DEBUG"

    class Config:
        """Pydantic 設定."""

        env_file = ".env"
        case_sensitive = False # 環境変数の大文字小文字を区別しない

    @property
    def database_url(self) -> str:
        """個別の要素からデータベース URL を組み立てる."""
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
