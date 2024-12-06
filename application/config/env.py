from pydantic_settings import BaseSettings


class PostgreSettings(BaseSettings):
    POSTGRES_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str


postgre_settings = PostgreSettings()
