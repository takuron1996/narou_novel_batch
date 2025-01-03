"""小説情報取得バッチ."""

import itertools

from prefect import flow, task

from apis.narou.narou_data import NarouData, NarouDataMapper
from apis.narou.type import NarouOfType, NarouOrderType, OutType
from apis.narou.urls import NarouURLBuilder
from apis.request import request_get
from batch.data import NcodeMappingData
from common.datetime_util import jst_now
from config.db import get_session
from config.log import console_logger
from models.author import get_author_id
from models.keyword import get_keyword_id
from repository.get_novel_data_repository import (
    get_target_novel_data,
    insert_author,
    insert_keyword,
    insert_novel,
    insert_novel_keywords,
)


@task(tags=["db"])
def get_target_from_db() -> list[NcodeMappingData]:
    """取得対象をDBから取得."""
    console_logger.info("取得対象をDBから取得")
    # 1-1 ncode_mappingとnovelテーブルから取得対象を取得
    console_logger.info(
        "task-1-1 ncode_mappingとnovelテーブルから取得対象を取得"
    )
    with get_session() as session:
        data_list = get_target_novel_data(session)

    # 1-2 取得したい小説のリストを作成
    # 1-3 return data_list
    console_logger.info("task-1-2 取得したい小説のリストを作成")
    return list(map(lambda x: NcodeMappingData(**x), data_list))


@task(retries=3, retry_delay_seconds=[5, 15, 30], tags=["api"])
def fetch_novel_info(data_list: list[NcodeMappingData]):
    """小説情報を取得."""
    console_logger.info("小説情報を取得")
    # 2-1 data_listを整形
    console_logger.info("task-2-1 data_listを整形")

    ## data_listが空リストの場合はそのまま返却
    if not data_list:
        console_logger.info("data_listが空のため処理を終了")
        return data_list
    ncode_list = list(map(lambda x: x.ncode, data_list))
    ncode = "-".join(ncode_list)

    # 2-2 なろうAPIから小説情報を取得
    ## t-u-n-w-bg-g-k-nt-ir-ibl-igl-izk-its-iti
    console_logger.info("task-2-2 なろうAPIから小説情報を取得")
    of_list = [
        NarouOfType.TITLE,
        NarouOfType.USERID,
        NarouOfType.NCODE,
        NarouOfType.WRITER,
        NarouOfType.BIGGENRE,
        NarouOfType.GENRE,
        NarouOfType.KEYWORD,
        NarouOfType.NOVELTYPE,
        NarouOfType.ISR15,
        NarouOfType.ISBL,
        NarouOfType.ISGL,
        NarouOfType.ISZANKOKU,
        NarouOfType.ISTENSEI,
        NarouOfType.ISTENNI,
    ]
    url = (
        NarouURLBuilder()
        .set_ncode(ncode)
        .set_order(NarouOrderType.NCODE_DESC)
        .set_output_format(OutType.JSON)
        .set_of_list(of_list)
        .set_limit(len(ncode_list))
        .build()
    )
    console_logger.debug(f"生成したURL: {url}")
    response = request_get(url)
    if response is None:
        console_logger.error("レスポンスが200以外のため終了")
        raise Exception("レスポンスが200以外のため終了")

    # 2-3 return insert_data_list
    return NarouDataMapper.map_response_to_data(response, data_list)


@task(tags=["db"])
def insert_novel_into_db(insert_data_list: list[NarouData]):
    """小説情報をDBへ登録."""
    # 3.1 insert_data_listをDB登録用に整形
    console_logger.info("task-3.1 insert_data_listをDB登録用に整形")
    insert_keyword_list = get_insert_keyword_list(insert_data_list)
    insert_author_novel_list = get_insert_author_novel_list(insert_data_list)
    insert_novel_keyword_list = get_insert_novel_keyword_list(insert_data_list)

    # 3.2 各テーブルにデータを登録
    console_logger.info("task-3.2 各テーブルにデータを登録")
    with get_session() as session:
        insert_keyword(session, insert_keyword_list)
        insert_author(session, insert_author_novel_list)
        insert_novel(session, insert_author_novel_list)
        insert_novel_keywords(session, insert_novel_keyword_list)

        # 全て登録された場合のみ適用
        session.commit()


def get_insert_keyword_list(insert_data_list: list[NarouData]):
    """keywordテーブルのデータ作成."""
    insert_keyword_set = set(
        itertools.chain.from_iterable(
            map(lambda x: x.keyword.split(), insert_data_list)
        )
    )
    return [
        {"keyword_id": get_keyword_id(), "name": keyword}
        for keyword in insert_keyword_set
    ]


def get_insert_author_novel_list(insert_data_list: list[NarouData]):
    """authorテーブルとnovelテーブルのデータ作成（useridは兼用）."""
    return [
        {
            # author用
            "userid": data.userid,
            "writer": data.writer,
            "author_id": get_author_id(),
            # novel用
            "id": data.id,
            "title": data.title,
            "biggenre_code": data.biggenre,
            "genre_code": data.genre,
            "novel_type_id": data.noveltype,
            "isr15": bool(data.isr15),
            "isbl": bool(data.isbl),
            "isgl": bool(data.isgl),
            "iszankoku": bool(data.iszankoku),
            "istensei": bool(data.istensei),
            "istenni": bool(data.istenni),
        }
        for data in insert_data_list
    ]


def get_insert_novel_keyword_list(insert_data_list: list[NarouData]):
    """novel_keywordsテーブルのデータ作成."""
    insert_novel_keyword_list = []
    for insert_data in insert_data_list:
        for keyword in insert_data.keyword.split():
            novel_keyword_data = {"id": insert_data.id}
            novel_keyword_data["keyword"] = keyword
            insert_novel_keyword_list.append(novel_keyword_data)
    return insert_novel_keyword_list


def generate_flow_run_name():
    """実行時の名前を生成."""
    date = jst_now().strftime("%Y%m%d")
    return f"get_novel_data_{date}"


def get_chunk_list(input_list: list, chunk_size: int):
    """指定されたサイズでリストを分割する関数.

    Parameters:
        input_list (list): 分割するリスト.
        chunk_size (int): 各チャンクのサイズ .

    Returns:
        list: 分割されたリストのリスト。
    """
    return [
        input_list[i : i + chunk_size]
        for i in range(0, len(input_list), chunk_size)
    ]


@flow(flow_run_name=generate_flow_run_name)
def get_novel_data():
    """小説情報取得バッチ."""
    # 1-1 get_target_from_dbを実行
    # 1回だけ実行
    # data_listが空の場合は終了
    console_logger.info("flow-1-1 get_target_from_dbを実行")
    data_list = get_target_from_db()
    if not data_list:
        console_logger.info("対象のデータが存在しないため、処理を終了")
        return

    # 1-2 fetch_novel_infoを実行
    # 500件ずつ区切って並列実行
    # (APIの最大取得件数が500件なため)
    console_logger.info("flow-1-2 fetch_novel_infoを実行")
    chunk_data_list = get_chunk_list(data_list, 500)
    fetch_data_list = fetch_novel_info.map(chunk_data_list).result()

    # 1-3 insert_novel_into_dbを実行
    # データをまとめて1回だけ実行
    console_logger.info("flow-1-3 insert_novel_into_dbを実行")
    insert_data_list = list(itertools.chain.from_iterable(fetch_data_list))
    insert_novel_into_db(insert_data_list)
