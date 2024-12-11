"""日刊ランキング取得バッチ"""

from datetime import datetime
from config.log import console_logger
import sys
from apis.narou.urls import NarouRankURLBuilder
from apis.narou.type import RankType
from apis.request import request_get
from apis.narou.narou_data import NarouRankDataMapper
from repository.daily_get_ranking_repository import ranking_insert


def process_command_args(args):
    """
    コマンド引数の処理を行う関数。

    Args:
        args (list): コマンド引数リスト（sys.argvの代わり）

    Returns:
        tuple: 有効なrank_date（yyyymmdd形式）とrank_type
        str: エラーが発生した場合は例外を発生させる
    """
    if len(args) > 0:
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
    if len(args) > 1:
        rank_type = args[1]
        try:
            rank_type = RankType(rank_type)
        except ValueError:
            raise ValueError(
                "無効なrank_typeが指定されました。許容される値: d, w, m, q"
            )
    else:
        # rank_typeが指定されていない場合は"d"をデフォルトとして設定
        rank_type = RankType.DAILY

    return rank_date, rank_type


def run(args, session):
    """
    メイン処理を実行する関数。

    Args:
        args (list): コマンド引数リスト（sys.argvの代わり）
        session: DBのインスタンス
    """
    ## コマンド引数の処理
    try:
        rank_date, rank_type = process_command_args(args)
        console_logger.debug(f"処理対象の日付: {rank_date}")
        console_logger.debug(f"処理対象の形式: {rank_type.name}")
    except ValueError as e:
        console_logger.error(f"{e}")
        sys.exit(1)

    ## なろうランキングAPIを叩く
    ###rank_dateを用いてURLを生成
    url = (
        NarouRankURLBuilder()
        .set_date(rank_date)
        .set_rank_type(rank_type)
        .build()
    )
    console_logger.debug(f"生成したURL: {url}")
    ###GET通信でなろうランキングAPIを叩く
    response = request_get(url)
    ####・レスポンスが200以外の場合はエラーとして終了
    if response is None:
        console_logger.error("レスポンスが200以外のため終了")
        sys.exit(1)
    ## DBに取得結果を入れる
    data = NarouRankDataMapper.map_response_to_data(response, rank_date)
    ranking_insert(session, data)
