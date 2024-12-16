"""このスクリプトは、コマンドラインから特定のコマンドを実行するためのものです.

コマンドライン引数に応じて、異なる機能を実行します。

使い方:
    python [スクリプト名] [コマンド]

利用可能なコマンド:
    init_db: 初期データ投入
    all_ranking: 全てのランキングを投入

注意:
    コマンドライン引数が適切でない場合、エラーメッセージを表示します。
"""

import sys

from command import all_ranking, init_db
from config.env import application_settings
from config.log import console_logger

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        console_logger.error("実行するコマンドを指定してください")
        sys.exit(1)
    if args[1] == "init_db":
        init_db.run(application_settings.INIT_DATA_PATH)
    elif args[1] == "all_ranking":
        all_ranking.run()
    else:
        console_logger.error(f"不明なコマンド: {args[1]}")
        sys.exit(1)
