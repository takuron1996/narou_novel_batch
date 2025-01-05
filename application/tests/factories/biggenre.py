"""biggenreのファクトリー関連."""

import factory

from models.biggenre import BigGenre


class BigGenreFactory(factory.alchemy.SQLAlchemyModelFactory):
    """biggenreのファクトリークラス."""

    class Meta:
        """メタデータ."""

        model = BigGenre
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"
