"""biggenre_genreのファクトリー関連."""

import factory

from models.biggenre_genre import BigGenreGenre


class BigGenreGenreFactory(factory.alchemy.SQLAlchemyModelFactory):
    """biggenre_genreのファクトリークラス."""

    class Meta:
        """メタデータ."""

        model = BigGenreGenre
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"
