"""genreのファクトリー関連."""

import factory

from models.genre import Genre


class GenreFactory(factory.alchemy.SQLAlchemyModelFactory):
    """genreのファクトリークラス."""

    class Meta:
        """メタデータ."""

        model = Genre
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"
