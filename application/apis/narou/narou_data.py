from dataclasses import dataclass
from config.log import console_logger
from datetime import datetime, date
import uuid


@dataclass
class NarouRankData:
    """ならうランキングAPIのレスポンスデータ"""

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


class NarouRankDataMapper:
    """APIレスポンスからNarouRankDataをマッピングするクラス"""

    @staticmethod
    def map_response_to_data(response, rank_date):
        """APIレスポンスからNarouRankDataのリストを生成するスタティックメソッド"""
        data_list = []
        try:
            for data in response.json():
                data["rank_date"] = datetime.strptime(
                    str(rank_date), "%Y%m%d"
                ).date()
                data["id"] = str(uuid.uuid4())
                data_list.append(NarouRankData(**data))
        except Exception as e:
            console_logger.error(
                "ならうランキングAPIのレスポンスデータのマッピングに失敗しました。"
            )
            raise ValueError(f"{e}")
        return data_list
