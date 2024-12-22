"""小説情報取得バッチのDB関連."""

from pathlib import Path

from sqlalchemy import text

from config.db import get_sql_query
from config.log import console_logger

base_dir = Path(__file__).parent
sub_dirs = ["sql", "get_novel_data_repository"]


def get_target_novel_data(session):
    """
    Retrieve novel data that exists in ncode_mapping but not in the novel table.
    
    Parameters:
        session (sqlalchemy.orm.Session): Database session object for executing queries
    
    Returns:
        List[Dict]: List of mappings containing novel data records. Each dictionary
                    represents a row from the query results.
    
    Notes:
        - Executes a SQL query defined in 'get_target_novel_data.sql'
        - Query results are returned as mapped dictionary objects
        - Uses SQLAlchemy text() for raw SQL execution
    """
    console_logger.debug("ncode_mappingにあり、novelにないデータを取得")
    sql_query = get_sql_query("get_target_novel_data.sql", base_dir, sub_dirs)
    return session.execute(text(sql_query)).mappings().all()
