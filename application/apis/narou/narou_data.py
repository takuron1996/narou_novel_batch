from dataclasses import dataclass
from config.log import console_logger


@dataclass
class NarouRankData:
    """ならうランキングAPIのレスポンスデータ"""

    ncode: str
    """nコード"""
    pt: int
    """ポイント"""
    rank: int
    """ランキング"""


class NarouRankDataMapper:
    """APIレスポンスからNarouRankDataをマッピングするクラス"""

    @staticmethod
    def map_response_to_data(response):
        """APIレスポンスからNarouRankDataのリストを生成するスタティックメソッド"""
        data_list = []
        try:
            for data in response.json():
                data_list.append(NarouRankData(**data))
        except Exception as e:
            console_logger.error(
                "ならうランキングAPIのレスポンスデータのマッピングに失敗しました。"
            )
            raise ValueError(f"{e}")
        return data_list
