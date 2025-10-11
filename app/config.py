from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore

_base_config = SettingsConfigDict(
    env_file="./.env", env_ignore_empty=True, extra="ignore"
)


class DatabaseSettings(BaseSettings):
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_PORT: Optional[int] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None

    REDIS_HOST: Optional[str] = None
    REDIS_PORT: Optional[int] = None

    model_config = _base_config

    @property
    def POSTGRES_URL(self) -> str:
        if (
            self.POSTGRES_USER is None
            or self.POSTGRES_PASSWORD is None
            or self.POSTGRES_SERVER is None
            or self.POSTGRES_PORT is None
            or self.POSTGRES_DB is None
        ):
            raise ValueError("Database settings are not fully configured")
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


class SecuritySettings(BaseSettings):
    JWT_SECRET: Optional[str] = None
    JWT_ALGORITHM: Optional[str] = None

    model_config = _base_config


class NotificationSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    model_config = _base_config


db_settings = DatabaseSettings()
security_settings = SecuritySettings()
notification_settings = NotificationSettings()  # type: ignore
