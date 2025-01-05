"""novel_typeのファクトリー関連."""

import factory

from models.novel_type import NovelType


class NovelTypeFactory(factory.alchemy.SQLAlchemyModelFactory):
    """novel_typeのファクトリークラス."""

    class Meta:
        """メタデータ."""

        model = NovelType
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"
