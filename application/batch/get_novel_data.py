"""小説情報取得バッチ."""

from dataclasses import dataclass

from prefect import task

from config.db import get_session
from config.log import console_logger
from repository.get_novel_data_repository import get_target_novel_data


@dataclass(frozen=True)
class NcodeMappingData:
    """ncodeのデータ."""

    id: str
    ncode: str


@task(tags=["db"])
def get_target_from_db() -> list[NcodeMappingData]:
    """
    Retrieve target novel data from the database and convert to NcodeMappingData objects.
    
    Parameters:
        None
    
    Returns:
        list[NcodeMappingData]: List of novel data objects mapped from database records
    
    Notes:
        Uses a database session to fetch records from ncode_mapping and novel tables,
        then converts the raw data into NcodeMappingData typed objects.
    """
    console_logger.info("取得対象をDBから取得")
    # 1-1 ncode_mappingとnovelテーブルから取得対象を取得
    console_logger.info("1-1 ncode_mappingとnovelテーブルから取得対象を取得")
    with get_session() as session:
        data_list = get_target_novel_data(session)

    # 1-2 取得したい小説のリストを作成
    # 1-3 return data_list
    console_logger.info("1-2 取得したい小説のリストを作成")
    return list(map(lambda x: NcodeMappingData(**x), data_list))
