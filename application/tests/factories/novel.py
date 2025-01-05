"""novelのファクトリー関連."""

import factory

from models.novel import Novel


class NovelFactory(factory.alchemy.SQLAlchemyModelFactory):
    """novelのファクトリークラス."""

    class Meta:
        """メタデータ."""

        model = Novel
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    title = factory.Sequence(lambda n: f"title_{n}")
    biggenre_code = 2
    genre_code = 201
    novel_type_id = 1
    isr15 = False
    isbl = False
    isgl = False
    iszankoku = False
    istensei = False
    istenni = False
