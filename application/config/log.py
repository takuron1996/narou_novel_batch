"""ロガー"""

import tomllib
from enum import Enum
from logging import getLogger
from logging.config import dictConfig
from pathlib import Path


class LoggerName(Enum):
    """ロガー名"""

    CONSOLE = "console"


def read_logger(filename):
    """ロガーの設定を読み込む

    Args:
        filename (str, optional): ログの設定ファイル（toml形式）
    """
    with open(filename, mode="rb") as file:
        dictConfig(tomllib.load(file).get("logging"))


def prepare_logger(output_directory="target", conf_file="log.toml"):
    """ロガーの事前準備

    Args:
        output_directory (str, optional): ログの出力先ディレクトリ
        conf_file (str, optional): ログの設定ファイル（toml形式）. defualt: log.toml
    """
    output_path = Path(output_directory)
    if not output_path.exists():
        output_path.mkdir()

    read_logger(conf_file)


prepare_logger()
console_logger = getLogger(LoggerName.CONSOLE.value)
