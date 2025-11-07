"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "ynym_portal"
    db_user: str = "username"
    db_password: str = "password"

    # JWT
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    # Environment
    environment: str = "development"
    log_level: str = "DEBUG"

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = False

    @property
    def database_url(self) -> str:
        """Build database URL from individual components."""
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
