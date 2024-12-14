"""DB関連の設定."""

from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from config.env import application_settings, postgre_settings
from config.log import console_logger


class SessionFactory:
    """同期セッション生成用のファクトリ."""

    @staticmethod
    def get_url(drivername="postgresql"):
        """接続先のURLを返却."""
        return URL.create(
            drivername=drivername,
            username=postgre_settings.POSTGRES_USER,
            password=postgre_settings.POSTGRES_PASSWORD,
            host=postgre_settings.POSTGRES_DB,
            database=postgre_settings.POSTGRES_NAME,
            port=5432,
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


def get_sql_query(file_name, base_dir=None, sub_dirs=None):
    """SQLファイルのパスからファイルの中身を取得する汎用関数。.

    Args:
        file_name (str): 読み込むSQLファイルの名前。
        base_dir (Path, optional): ベースディレクトリ。
            デフォルトは現在のスクリプトのディレクトリ。
        sub_dirs (list[str], optional): サブディレクトリのリスト。

    Returns:
        str: SQLファイルの内容。

    Raises:
        FileNotFoundError: ファイルが見つからない場合に例外をスロー。
    """
    if base_dir is None:
        base_dir = Path(__file__).parent
    else:
        base_dir = Path(base_dir)

    # サブディレクトリを結合
    if sub_dirs:
        file_path = base_dir.joinpath(*sub_dirs, file_name)
    else:
        file_path = base_dir / file_name

    # ファイルを読み込み
    if not file_path.exists():
        console_logger.error(f"SQLファイルが見つかりません: {file_path}")
        raise FileNotFoundError(f"SQL file not found: {file_path}")

    console_logger.debug(f"ファイルを読み込みます: {file_path}")
    with file_path.open("r", encoding="utf-8") as file:
        return file.read()
