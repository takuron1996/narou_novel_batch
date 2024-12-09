from sqlalchemy import text
from pathlib import Path
from dataclasses import asdict


def ranking_insert(session, narou_rank_data_list):
    """ならうランキングデータを投入"""
    current_dir = Path(__file__).parent
    file_path = (
        current_dir
        / "sql"
        / "daily_get_ranking_repository"
        / "ranking_insert_ncode_mapping.sql"
    )
    params = tuple(map(asdict, narou_rank_data_list))
    with file_path.open("r") as file:
        sql_query = file.read()
        session.execute(
            text(sql_query).bindparams(ncode="ncode").bindparams(id="id"),
            params,
        )
    file_path = (
        current_dir
        / "sql"
        / "daily_get_ranking_repository"
        / "ranking_insert_rank.sql"
    )
    with file_path.open("r") as file:
        sql_query = file.read()
        session.execute(
            text(sql_query)
            .bindparams(id="id")
            .bindparams(rank="rank")
            .bindparams(rank_date="rank_date"),
            params,
        )
        session.commit()
