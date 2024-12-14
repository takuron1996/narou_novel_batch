"""ロガー."""

import tomllib
from enum import Enum
from logging import getLogger
from logging.config import dictConfig
from config.env import application_settings

class LoggerName(Enum):
    """ロガー名."""

    CONSOLE = "console"


def read_logger(filename):
    """ロガーの設定を読み込む.

    Args:
        filename (str, optional): ログの設定ファイル（toml形式）
    """
    with open(filename, mode="rb") as file:
        dictConfig(tomllib.load(file).get("logging"))


read_logger(application_settings.LOG_CONFIG_PATH)
console_logger = getLogger(LoggerName.CONSOLE.value)
