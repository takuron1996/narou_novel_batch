"""なろうAPIのランキング関連."""

import uuid
from dataclasses import dataclass
from datetime import date, datetime

from config.log import console_logger


@dataclass
class NarouRankData:
    """ならうランキングAPIのレスポンスデータ."""

    ncode: str
    """nコード"""
    pt: int
    """ポイント"""
    rank: int
    """ランキング"""
    rank_date: date
    """取得に指定した日時"""
    id: str
    """uuid"""
    rank_type: str
    """ランクの形式"""


class NarouRankDataMapper:
    """APIレスポンスからNarouRankDataをマッピングするクラス."""

    @staticmethod
    def map_response_to_data(response, rank_date, rank_type):
        """APIレスポンスからNarouRankDataのリストを生成するスタティックメソッド."""
        data_list = []
        try:
            for data in response.json():
                data["rank_date"] = datetime.strptime(
                    str(rank_date), "%Y%m%d"
                ).date()
                data["id"] = str(uuid.uuid4())
                data["rank_type"] = rank_type.value
                data_list.append(NarouRankData(**data))
        except Exception as e:
            console_logger.error(
                "ならうランキングAPIのレスポンスデータのマッピングに失敗しました。"
            )
            raise ValueError(f"{e}")
        return data_list
