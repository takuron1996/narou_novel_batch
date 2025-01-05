"""エントリポイント."""

from prefect import serve

from batch.get_novel_data import get_novel_data
from batch.get_ranking import get_ranking

if __name__ == "__main__":
    # cronはUTC前提で記述

    # get_rankingの設定
    # 毎日、日本時間の23:00に実行予定
    daily_get_ranking = get_ranking.to_deployment(
        name="daily_get_ranking",
        cron="0 14 * * *",
        parameters={"rank_type": "d"},
    )

    # 火曜日、日本時間の23:00に実行予定
    weekly_get_ranking = get_ranking.to_deployment(
        name="weekly_get_ranking",
        cron="0 14 * * 2",
        parameters={"rank_type": "w"},
    )

    # 1日、日本時間の23:00に実行予定
    monthly_get_ranking = get_ranking.to_deployment(
        name="monthly_get_ranking",
        cron="0 14 1 * *",
        parameters={"rank_type": "m"},
    )

    # 1,4,7,10月の1日、日本時間の23:00に実行予定
    quarterly_get_ranking = get_ranking.to_deployment(
        name="quarterly_get_ranking",
        cron="0 14 1 1,4,7,10 *",
        parameters={"rank_type": "q"},
    )

    # get_novel_dataの設定
    # 毎日、日本時間の23:30に実行予定
    daily_get_novel_data = get_novel_data.to_deployment(
        name="daily_get_novel_data",
        cron="30 14 * * *",
    )

    # 起動
    serve(
        daily_get_ranking,
        weekly_get_ranking,
        monthly_get_ranking,
        quarterly_get_ranking,
        daily_get_novel_data,
    )
