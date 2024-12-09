# narou_novel_batch
なろう小説のAPIに対してバッチ処理を実施

## 1. 開発環境構築

### 環境変数

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
