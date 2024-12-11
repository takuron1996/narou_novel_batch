# narou_novel_batch
なろう小説のAPIに対してバッチ処理を実施

# 環境変数

開発環境をセットアップする前に、以下の環境変数を設定する必要があります。  
`.env`ファイルをプロジェクトのルートディレクトリに作成し、以下の内容を参考に設定ください。

| 環境変数名          | 説明                   | ローカルでの推奨値        |
|-------------------|----------------------|-------------------------|
| `POSTGRES_NAME`   | Postgresのデータベース名 | `postgres`              |
| `POSTGRES_USER`   | Postgresのユーザー名    | `postgres`              |
| `POSTGRES_PASSWORD` | Postgresのパスワード    | `postgres`              |
| `POSTGRES_HOST`   | Postgresのホスト名     | `db`                    |
| `POSTGRES_PORT`   | Postgresのポート番号    | `5432`                  |
| `DEBUG`   | DEBUGモードで起動するかどうか（TRUEはDEBUGモード）    | `true`                  |

# Makefile コマンド説明

| コマンド       | 説明                                                                                           |
|----------------|------------------------------------------------------------------------------------------------|
| `init_db`     | `command.py` の `init_db` コマンドを実行してデータベースを初期化します。                         |
| `test`        | `pytest` を使用してテストを実行します。カバレッジレポートを生成し、結果をHTMLで出力します。       |
| `up`          | Dockerコンテナをバックグラウンドで起動します。                                                   |
| `build`       | Dockerイメージをビルドします。                                                                 |
| `down`        | 起動中のDockerコンテナを停止し、削除します。                                                     |
| `check`       | `black`と`ruff`を使用してコードスタイルや静的解析を行います。`ruff`では自動修正を試みます。       |
| `install`     | `poetry install` を実行して必要な依存ライブラリをインストールします。                             |
| `update`      | `poetry update` を実行して依存ライブラリを最新バージョンに更新します。                           |
| `migration`   | `alembic` を使用して新しいマイグレーションファイルを自動生成します。                              |
| `upgrade`     | `alembic` を使用してデータベースを最新のスキーマにアップグレードします。                         |

# 初期データについて

## 実行されるSQLの場所

- `init_db` コマンドでは、`application/init_data` ディレクトリ以下に格納された `.sql` ファイルが順次実行されます。

## SQLファイルの命名規則

SQLファイルは以下の命名規則に従う必要があります：

### 形式

<数値>.<説明>.sql


### 各要素の詳細
1. **数値部分**:
   - ファイルの実行順序を決定する番号です。
   - 整数値で、0から始まる数字や負数は使用しないでください。
   - 例: `1`, `2`, `10`

2. **説明部分**:
   - SQLファイルの内容を簡潔に説明する短い文字列。
   - 英数字とアンダースコア（`_`）のみ使用してください。
   - スペースや特殊文字は避けてください。
   - 例: `create_tables`, `insert_data`, `update_schema`

3. **拡張子**:
   - ファイルの拡張子は必ず `.sql` である必要があります。

### 命名例
- `1.create_tables.sql`: テーブル作成用のSQLスクリプト
- `2.insert_data.sql`: 初期データ投入用のSQLスクリプト
- `10.update_schema.sql`: スキーマ更新用のSQLスクリプト

### 注意事項
- 数値部分が重複している場合、どちらが先に実行されるかは保証されません。
- 命名規則に従わないファイルはスクリプトの実行対象外となる可能性があります。

## 実行順序

- ファイル名の先頭に含まれる数値で昇順に実行されます。
  - 例: `1.create_tables.sql` → `2.insert_data.sql` → `10.update_schema.sql`
- ファイルが多い場合でも、数値に基づく順序で正しく処理されます。

## 注意事項

- **実行環境**:
  - `application/init_data` ディレクトリにすべての必要なSQLファイルが存在することを確認してください。
- **影響範囲**:
  - SQLファイルは直接データベースに変更を加えるため、内容を事前に確認し、バックアップを取得してから実行してください。
- **命名エラーの確認**:
  - 命名エラーや形式の不備がある場合、コマンドがエラーとなる可能性があります。
