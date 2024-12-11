import factory
from models.rank import Rank
import datetime


class RankFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Rank

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
