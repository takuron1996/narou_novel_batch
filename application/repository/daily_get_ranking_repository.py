from sqlalchemy import text
from pathlib import Path
from dataclasses import asdict
from config.db import get_sql_query
from config.log import console_logger

base_dir = Path(__file__).parent
sub_dirs = ["sql", "daily_get_ranking_repository"]


def ranking_insert(session, narou_rank_data_list):
    """ならうランキングデータを投入"""
    params = tuple(map(asdict, narou_rank_data_list))

    console_logger.debug("nocde_mappingの登録")
    sql_query = get_sql_query(
        "ranking_insert_ncode_mapping.sql", base_dir, sub_dirs
    )
    session.execute(
        text(sql_query).bindparams(ncode="ncode").bindparams(id="id"),
        params,
    )

    console_logger.debug("rankの登録")
    sql_query = get_sql_query("ranking_insert_rank.sql", base_dir, sub_dirs)
    session.execute(
        text(sql_query)
        .bindparams(id="id")
        .bindparams(rank="rank")
        .bindparams(rank_date="rank_date")
        .bindparams(rank_type="rank_type"),
        params,
    )
    session.commit()
