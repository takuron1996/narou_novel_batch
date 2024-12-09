from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from config.env import postgre_settings, application_settings
from contextlib import contextmanager


class SessionFactory:
    """同期セッション生成用のファクトリ."""

    @staticmethod
    def get_url(drivername="postgresql"):
        """接続先のURLを返却."""
        return URL.create(
            drivername=drivername,
            username=postgre_settings.POSTGRES_USER,
            password=postgre_settings.POSTGRES_PASSWORD,
            host=postgre_settings.POSTGRES_HOST,
            database=postgre_settings.POSTGRES_NAME,
            port=postgre_settings.POSTGRES_PORT,
        )

    @classmethod
    def create(cls):
        """セッションを生成."""
        if not hasattr(cls, "_session_factory"):
            engine = create_engine(
                cls.get_url(), echo=application_settings.DEBUG
            )
            cls._session_factory = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine,
            )
        return cls._session_factory


@contextmanager
def get_session():
    """DBの同期セッションインスタンスを返却."""
    session = SessionFactory.create()()
    try:
        yield session
    finally:
        session.close()
