"""novel_keywordsのファクトリー関連."""

import factory

from models.novel_keywords import NovelKeywords


class NovelKeywordsFactory(factory.alchemy.SQLAlchemyModelFactory):
    """novel_keywordsのファクトリークラス."""

    class Meta:
        """メタデータ."""

        model = NovelKeywords
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"
