"""なろうAPIのランキング関連."""

import uuid
from dataclasses import dataclass
from datetime import date

from batch.data import NcodeMappingData
from common.datetime_util import jst_strptime
from config.log import console_logger

# なろうAPI関連


@dataclass(frozen=True)
class NarouData:
    """なろうAPIのレスポンスデータ."""

    id: str
    title: str
    userid: int
    ncode: str
    writer: str
    biggenre: int
    genre: int
    keyword: str
    noveltype: int
    isr15: int
    isbl: int
    isgl: int
    iszankoku: int
    istensei: int
    istenni: int


class NarouDataMapper:
    """APIレスポンスからNarouDataをマッピングするクラス."""

    @staticmethod
    def map_response_to_data(
        response, ncode_mapping_data_list: list[NcodeMappingData]
    ) -> list[NarouData]:
        """APIレスポンスからNarouDataのリストを生成するスタティックメソッド."""
        data_list = []
        try:
            for data in response.json()[1:]:
                ncode_mapping_data = [
                    n.id
                    for n in ncode_mapping_data_list
                    if n.ncode == data["ncode"]
                ]
                if not len(ncode_mapping_data) == 1:
                    console_logger.warning("対応するncodeが含まれていません。")
                    continue
                data["id"] = ncode_mapping_data[0]
                data_list.append(NarouData(**data))
        except Exception as e:
            console_logger.error(
                "なろうAPIのレスポンスデータのマッピングに失敗しました。"
            )
            raise ValueError(f"{e}")
        return data_list


# なろうランキングAPI関連


@dataclass(frozen=True)
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
    def map_response_to_data(response, rank_date, rank_type) -> NarouRankData:
        """APIレスポンスからNarouRankDataのリストを生成するスタティックメソッド."""
        data_list = []
        try:
            for data in response.json():
                data["rank_date"] = jst_strptime(str(rank_date)).date()
                data["id"] = str(uuid.uuid4())
                data["rank_type"] = rank_type.value
                data_list.append(NarouRankData(**data))
        except Exception as e:
            console_logger.error(
                "なろうランキングAPIのレスポンスデータのマッピングに失敗しました。"
            )
            raise ValueError(f"{e}")
        return data_list
