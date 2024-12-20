"""環境変数関連."""

from pydantic_settings import BaseSettings


class ApplicationSettings(BaseSettings):
    """アプリケーション全体の設定を管理するクラス."""

    DEBUG: bool = False
    LOG_CONFIG_PATH: str = "log.toml"
    INIT_DATA_PATH: str = "./init_data"


class PostgreSettings(BaseSettings):
    """PostgreSQLデータベースの接続設定を管理するクラス."""

    POSTGRES_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str


application_settings = ApplicationSettings()
postgre_settings = PostgreSettings()
