"""keywordのファクトリー関連."""

import factory

from models.keyword import Keyword, get_keyword_id


class KeywordFactory(factory.alchemy.SQLAlchemyModelFactory):
    """keywordのファクトリークラス."""

    class Meta:
        """メタデータ."""

        model = Keyword
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    keyword_id = factory.LazyFunction(lambda: get_keyword_id())
    name = factory.Sequence(lambda n: f"name_{n}")
