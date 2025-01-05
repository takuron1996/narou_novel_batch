"""rankのファクトリー関連."""

import factory

from models.rank import Rank


class RankFactory(factory.alchemy.SQLAlchemyModelFactory):
    """rankのファクトリクラス."""

    class Meta:
        """メタデータ."""

        model = Rank
        sqlalchemy_session = None  # セッションを初期化
        sqlalchemy_session_persistence = "commit"  # データをコミットする
