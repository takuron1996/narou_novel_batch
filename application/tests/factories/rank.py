"""rankのファクトリー関連."""
import datetime

import factory

from models.rank import Rank


class RankFactory(factory.alchemy.SQLAlchemyModelFactory):
    """rankのファクトリクラス."""
    class Meta:
        """メタデータ."""
        model = Rank
        sqlalchemy_session = None  # セッションを初期化
        sqlalchemy_session_persistence = "commit"  # データをコミットする

    id = factory.SubFactory(
        "tests.factories.NcodeMappingFactory"
    )  # 外部キーとしてNcodeMappingを生成
    rank = factory.Sequence(lambda n: n + 1)  # 順位を1から順に生成
    rank_date = factory.LazyFunction(
        lambda: datetime.date.today()
    )  # 今日の日付を生成
    created_at = factory.LazyFunction(
        lambda: datetime.datetime.now()
    )  # 現在時刻を使用
    updated_at = factory.LazyFunction(
        lambda: datetime.datetime.now()
    )  # 現在時刻を使用
    deleted_at = None
