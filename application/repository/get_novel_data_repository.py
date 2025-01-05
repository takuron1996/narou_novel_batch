"""小説情報取得バッチのDB関連."""

from pathlib import Path

from sqlalchemy import text

from config.db import get_sql_query
from config.log import console_logger

base_dir = Path(__file__).parent
sub_dirs = ["sql", "get_novel_data_repository"]


def get_target_novel_data(session) -> list[dict]:
    """ncode_mappingにあり、novelにないデータを取得."""
    console_logger.debug("ncode_mappingにあり、novelにないデータを取得")
    sql_query = get_sql_query("get_target_novel_data.sql", base_dir, sub_dirs)
    return session.execute(text(sql_query)).mappings().all()


def insert_keyword(session, insert_keyword_list: list[dict]):
    """キーワードを登録."""
    console_logger.info("keywordにデータを登録")
    sql_query = get_sql_query("insert_keyword.sql", base_dir, sub_dirs)
    session.execute(text(sql_query), insert_keyword_list)


def insert_author(session, insert_author_list: list[dict]):
    """作者を登録."""
    console_logger.info("authorにデータを登録")
    sql_query = get_sql_query("insert_author.sql", base_dir, sub_dirs)
    session.execute(text(sql_query), insert_author_list)


def insert_novel(session, insert_novel_list: list[dict]):
    """小説を登録."""
    console_logger.info("novelにデータを登録")
    sql_query = get_sql_query("insert_novel.sql", base_dir, sub_dirs)
    session.execute(text(sql_query), insert_novel_list)


def insert_novel_keywords(session, insert_novel_keyword_list: list[dict]):
    """小説とキーワードの中間テーブルを登録."""
    console_logger.info("novel_keywordsにデータを登録")
    sql_query = get_sql_query("insert_novel_keyword.sql", base_dir, sub_dirs)
    session.execute(text(sql_query), insert_novel_keyword_list)
