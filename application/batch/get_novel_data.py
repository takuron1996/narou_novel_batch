"""小説情報取得バッチ."""

from prefect import task

from apis.narou.narou_data import NarouDataMapper
from apis.narou.type import NarouOfType, NarouOrderType, OutType
from apis.narou.urls import NarouURLBuilder
from apis.request import request_get
from batch.data import NcodeMappingData
from config.db import get_session
from config.log import console_logger
from repository.get_novel_data_repository import get_target_novel_data


@task(tags=["db"])
def get_target_from_db() -> list[NcodeMappingData]:
    """取得対象をDBから取得."""
    console_logger.info("取得対象をDBから取得")
    # 1-1 ncode_mappingとnovelテーブルから取得対象を取得
    console_logger.info("1-1 ncode_mappingとnovelテーブルから取得対象を取得")
    with get_session() as session:
        data_list = get_target_novel_data(session)

    # 1-2 取得したい小説のリストを作成
    # 1-3 return data_list
    console_logger.info("1-2 取得したい小説のリストを作成")
    return list(map(lambda x: NcodeMappingData(**x), data_list))


@task(retries=3, retry_delay_seconds=[5, 15, 30], tags=["api"])
def fetch_novel_info(data_list: list[NcodeMappingData]):
    """小説情報を取得."""
    console_logger.info("小説情報を取得")
    # 2-1 data_listを整形
    console_logger.info("2-1 data_listを整形")
    ncode_list = list(map(lambda x: x.ncode, data_list))
    ncode = "-".join(ncode_list)

    # 2-2 なろうAPIから小説情報を取得
    # t-u-n-w-bg-g-k-nt-ir-ibl-igl-izk-its-iti
    console_logger.info("2-2 なろうAPIから小説情報を取得")
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
        .set_order(NarouOrderType.NCODEDESC)
        .set_output_format(OutType.JSON)
        .set_of_list(of_list)
        .build()
    )
    console_logger.info(f"生成したURL: {url}")
    response = request_get(url)
    if response is None:
        console_logger.error("レスポンスが200以外のため終了")
        raise Exception("レスポンスが200以外のため終了")

    # 2-3 return insert_data_list
    return NarouDataMapper.map_response_to_data(response, data_list)
