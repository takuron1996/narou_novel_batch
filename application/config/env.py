from pydantic_settings import BaseSettings


class ApplicationSettings(BaseSettings):
    DEBUG: bool


class PostgreSettings(BaseSettings):
    POSTGRES_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str


application_settings = ApplicationSettings()
postgre_settings = PostgreSettings()
