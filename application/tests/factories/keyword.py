"""keywordのファクトリー関連."""

import uuid

import factory

from models.keyword import Keyword


class KeywordFactory(factory.alchemy.SQLAlchemyModelFactory):
    """keywordのファクトリークラス."""

    class Meta:
        """メタデータ."""

        model = Keyword
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    keyword_id = factory.LazyFunction(lambda: uuid.uuid4())
    name = factory.Sequence(lambda n: f"name_{n}")
