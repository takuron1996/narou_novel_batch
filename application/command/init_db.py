"""DB初期データ投入用.

このモジュールは指定されたディレクトリ内にあるSQLファイルを順番に読み込み、
それらのクエリをデータベースに実行する機能を提供します。

主な機能:
1. 指定ディレクトリ以下のSQLファイルを再帰的に取得。
2. ファイル名に基づいてSQLファイルをソート。
3. ソートされたSQLクエリをデータベースセッションで順次実行。
"""

from pathlib import Path

from sqlalchemy import text

from config.db import get_session


def run(directory_path):
    """対象ディレクトリ以下のSQLファイルをすべて実行する。.

    ディレクトリ内のSQLファイルを読み込み、ファイル名の先頭にある
    数字部分でソートした後、データベースセッションを使用して順次クエリを実行する。

    Args:
        directory_path (str or Path): SQLファイルを含む対象のディレクトリパス。
    """
    with get_session() as session:
        for _, sql_query in read_all_files_in_directory(directory_path):
            session.execute(text(sql_query))
        session.commit()


def read_all_files_in_directory(directory_path):
    """指定されたディレクトリ以下のすべてのSQLファイルを読み込む.

    内容はファイルパスとともにジェネレーターで逐次返す.

    SQLファイルは、ファイル名の先頭にある数字部分でソートされます。
    ファイル名形式が「数字.文字列.sql」であることを想定しています。

    Args:
        directory_path (str or Path): 対象のディレクトリパス。

    Yields:
        tuple: (file_path, file_content)
            - file_path (Path): SQLファイルのパス。
            - file_content (str): SQLファイルの内容。

    Raises:
        ValueError: 指定されたパスが有効なディレクトリでない場合。
    """

    def extract_number(file_path):
        """ファイル名から先頭の数字部分を抽出する。.

        Args:
            file_path (Path): 対象のファイルパス。

        Returns:
            int: ファイル名に含まれる先頭の数字部分。

        Raises:
            ValueError: ファイル名に数字が含まれていない場合。
        """
        stem = file_path.stem  # ファイル名（拡張子なし）
        number_part = stem.split(".")[0]  # 数字部分を抽出
        return int(number_part)  # 数字部分を整数として返す

    try:
        directory = Path(directory_path)
        if not directory.is_dir():
            raise ValueError(f"{directory_path} is not a valid directory")

        for file_path in sorted(directory.rglob("*.sql"), key=extract_number):
            try:
                with file_path.open("r") as f:
                    yield file_path, f.read()  # ファイルパスと内容をジェネレーターで返す
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")
    except Exception as e:
        print(f"Error processing the directory {directory_path}: {e}")
