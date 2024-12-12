"""環境変数関連."""
from pydantic_settings import BaseSettings


class ApplicationSettings(BaseSettings):
    """アプリケーション全体の設定を管理するクラス."""
    DEBUG: bool


class PostgreSettings(BaseSettings):
    """PostgreSQLデータベースの接続設定を管理するクラス."""
    POSTGRES_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str


application_settings = ApplicationSettings()
postgre_settings = PostgreSettings()
