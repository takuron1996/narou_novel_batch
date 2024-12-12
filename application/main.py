from batch.get_ranking import get_ranking

if __name__ == "__main__":
    #  全て取得のローカル起動用
    # get_ranking("20241001", "")
    get_ranking.serve(cron="1 15 * * *", pause_on_shutdown=False)
