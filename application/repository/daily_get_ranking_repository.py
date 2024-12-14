"""なろうランキングデータ投入関連."""
from dataclasses import asdict
from pathlib import Path

from sqlalchemy import text

from config.db import get_sql_query
from config.log import console_logger

base_dir = Path(__file__).parent
sub_dirs = ["sql", "daily_get_ranking_repository"]


def ranking_insert(session, narou_rank_data_list):
    """ならうランキングデータを投入."""
    try:
        params = tuple(map(asdict, narou_rank_data_list))

        console_logger.debug("nocde_mappingの登録")
        sql_query = get_sql_query(
            "ranking_insert_ncode_mapping.sql", base_dir, sub_dirs
        )
        session.execute(
            text(sql_query),
            params,
        )

        console_logger.debug("rankの登録")
        sql_query = get_sql_query("ranking_insert_rank.sql", base_dir, sub_dirs)
        session.execute(
            text(sql_query),
            params,
        )
        session.commit()
    except Exception as e:
        session.rollback()
        console_logger.error("ランキングデータの登録に失敗しました。")
        raise e
