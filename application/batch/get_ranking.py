"""日刊ランキング取得バッチ."""

import sys
from datetime import datetime

from prefect import flow, task
from prefect.runtime import flow_run

from apis.narou.narou_data import NarouRankDataMapper
from apis.narou.type import RankType
from apis.narou.urls import NarouRankURLBuilder
from apis.request import request_get
from config.db import get_session
from config.log import console_logger
from repository.daily_get_ranking_repository import ranking_insert


def process_command_args(args):
    """コマンド引数の処理を行う関数。.

    Args:
        args (list): コマンド引数リスト（sys.argvの代わり）

    Returns:
        tuple: 有効なrank_date（yyyymmdd形式）とrank_type_tuple
        str: エラーが発生した場合は例外を発生させる
    """
    if len(args) > 0 and args[0]:
        rank_date = args[0]
        try:
            # 日付形式の確認
            parsed_date = datetime.strptime(rank_date, "%Y%m%d")
            # 未来日のチェック
            if parsed_date > datetime.now():
                raise ValueError("rank_dateは未来日を指定できません。")
        except ValueError as e:
            raise ValueError(f"無効なrank_dateが指定されました: {e}")
    else:
        # 引数が指定されていない場合は現在日時を使用
        rank_date = datetime.now().strftime("%Y%m%d")

    # rank_typeの処理
    rank_type_list = []
    if len(args) > 1 and args[1]:
        rank_type = args[1]
        try:
            rank_type_list.append(RankType(rank_type))
        except ValueError:
            raise ValueError(
                "無効なrank_typeが指定されました。許容される値: d, w, m, q"
            )
    else:
        # rank_typeが指定されていない場合は使用できる全てを設定
        rank_type_list.append(RankType.DAILY)
        for rank_type in (
            RankType.WEEKLY,
            RankType.MONTHLY,
            RankType.QUARTERLY,
        ):
            if RankType.is_valid_date_for_rank_type(rank_type, rank_date):
                rank_type_list.append(rank_type)
    return rank_date, rank_type_list


def generate_flow_run_name():
    parameters = flow_run.parameters
    rank_date = parameters["rank_date"]
    if not rank_date:
        rank_date = datetime.now().strftime("%Y%m%d")
    rank_type = parameters["rank_type"]
    if not rank_type:
        rank_type = "all"
    return f"get_ranking_{rank_date}-{rank_type}"


@task
def task_command_line(args):
    """コマンド引数の処理."""
    console_logger.info("コマンド引数の処理")
    try:
        rank_date, rank_type_list = process_command_args(args)
        console_logger.info(f"処理対象の日付: {rank_date}")
        console_logger.info(
            f"処理対象の形式: {tuple(map(lambda x: x.name, rank_type_list))}"
        )
    except ValueError as e:
        console_logger.error(f"{e}")
        sys.exit(1)
    return rank_date, rank_type_list


@task(retries=3, retry_delay_seconds=[5, 15, 30], tags=["api"])
def get_api(rank_date, rank_type):
    """なろうランキングAPIを叩く."""
    console_logger.info("なろうランキングAPIを叩く")
    # rank_dateを用いてURLを生成
    url = (
        NarouRankURLBuilder()
        .set_date(rank_date)
        .set_rank_type(rank_type)
        .build()
    )
    console_logger.info(f"生成したURL: {url}")
    # GET通信でなろうランキングAPIを叩く
    response = request_get(url)
    # ・レスポンスが200以外の場合はエラーとして終了
    if response is None:
        console_logger.error("レスポンスが200以外のため終了")
        sys.exit(1)
    return response


@task(tags=["db"])
def insert_db(response, rank_date, rank_type):
    """DBに取得結果を入れる."""
    console_logger.info("DBに取得結果を入れる")
    data = NarouRankDataMapper.map_response_to_data(
        response, rank_date, rank_type
    )
    with get_session() as session:
        ranking_insert(session, data)


@flow(flow_run_name=generate_flow_run_name)
def get_ranking(rank_date="", rank_type=""):
    """ランキングを取得してDBに蓄積.

    Args:
        rank_date (str, optional): ランキングの対象となる日付を "yyyymmdd" 形式で指定します。
            - 未指定の場合は現在日時が使用されます。
            - 以下の制約があります:
                1. `rank_date` は2013年5月1日以降の日付である必要があります。
                2. 未来日を指定した場合はエラーになります。
                3. "yyyymmdd" 形式以外の場合はエラーになります。
                4. 週間ランキングを取得する場合、日付は火曜日の日付を指定してください。
                5. 月間・四半期ランキングを取得する場合、日付は1日を指定してください。
        rank_type (str, optional): ランキングの種類を指定します。
            - 指定なしの場合は、取得できるランキング全てを取得。
            - 想定される値は以下の通りです:
                "d" - 日間
                "w" - 週間
                "m" - 月間
                "q" - 四半期
            - 上記以外の値を指定した場合はエラーになります。
    """
    rank_date, rank_type_list = task_command_line([rank_date, rank_type])
    for rank_type in rank_type_list:
        response = get_api(rank_date, rank_type)
        insert_db(response, rank_date, rank_type)
