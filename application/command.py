"""このスクリプトは、コマンドラインから特定のコマンドを実行するためのものです.

コマンドライン引数に応じて、異なる機能を実行します。

使い方:
    python [スクリプト名] [コマンド]

利用可能なコマンド:
    init_db: 初期データ投入

注意:
    コマンドライン引数が適切でない場合、エラーメッセージを表示します。
"""

import sys

from command.init_db import run
from config.log import console_logger

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        console_logger.error("実行するコマンドを指定してください")
        sys.exit(1)
    if args[1] == "init_db":
        run("./init_data")
    else:
        console_logger.error(f"不明なコマンド: {args[1]}")
        sys.exit(1)
