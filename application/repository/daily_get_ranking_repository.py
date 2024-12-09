from sqlalchemy import text
from pathlib import Path
from dataclasses import asdict


def get_sql_query(file_name):
    """SQLファイルのパスからファイルの中身を取得"""
    current_dir = Path(__file__).parent
    file_path = current_dir / "sql" / "daily_get_ranking_repository" / file_name
    with file_path.open("r") as file:
        return file.read()


def ranking_insert(session, narou_rank_data_list):
    """ならうランキングデータを投入"""
    params = tuple(map(asdict, narou_rank_data_list))

    # nocde_mappingの登録
    sql_query = get_sql_query("ranking_insert_ncode_mapping.sql")
    session.execute(
        text(sql_query).bindparams(ncode="ncode").bindparams(id="id"),
        params,
    )

    # rankの登録
    sql_query = get_sql_query("ranking_insert_rank.sql")
    session.execute(
        text(sql_query)
        .bindparams(id="id")
        .bindparams(rank="rank")
        .bindparams(rank_date="rank_date"),
        params,
    )
    session.commit()
