from prefect import serve

from batch.get_ranking import get_ranking

if __name__ == "__main__":
    #  全て取得のローカル起動用
    # get_ranking("20241001", "")

    daily_get_ranking = get_ranking.to_deployment(name="daily_get_ranking", cron="5 15 * * *",parameters={"rank_type": "d"})
    weekly_get_ranking = get_ranking.to_deployment(name="weekly_get_ranking", cron="5 15 * * 2",  parameters={"rank_type": "w"})
    monthly_get_ranking = get_ranking.to_deployment(name="monthly_get_ranking", cron="5 15 1 * *", parameters={"rank_type": "m"})
    quarterly_get_ranking = get_ranking.to_deployment(name="quarterly_get_ranking", cron="5 15 1 * *", parameters={"rank_type": "q"})
    serve(daily_get_ranking, weekly_get_ranking, monthly_get_ranking, quarterly_get_ranking)
