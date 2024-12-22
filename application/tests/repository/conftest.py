"""参考: https://tech.salesnow.jp/entry/pytest-with-clean-db."""

from importlib import import_module
from pathlib import Path

import pytest
from pytest_postgresql import factories
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

from models.base import Base
from tests.factories.author import AuthorFactory
from tests.factories.biggenre import BigGenreFactory
from tests.factories.biggenre_genre import BigGenreGenreFactory
from tests.factories.genre import GenreFactory
from tests.factories.keyword import KeywordFactory
from tests.factories.ncode_mapping import NcodeMappingFactory
from tests.factories.novel import NovelFactory
from tests.factories.novel_keywords import NovelKeywordsFactory
from tests.factories.novel_type import NovelTypeFactory
from tests.factories.rank import RankFactory
from tests.factories.rank_type import RankTypeFactory


def import_migration_module(module):
    """マイグレーションに含めたいモジュールをimport."""
    for file_name in (p.name for p in Path(module).iterdir() if p.is_file()):
        if file_name in {"__init__.py", "base.py"}:
            continue
        file_name = file_name.replace(".py", "")
        import_module(f"{module}.{file_name}")


# Base.metadata.create_all(engine)はimportしていないとテーブルを作成しないため実施
import_migration_module("models")
postgresql_in_docker = factories.postgresql_noproc()
postgresql_fixture = factories.postgresql("postgresql_in_docker")


def init_rank_type():
    """rank_typeの初期データ."""
    for type in ("d", "w", "m", "q"):
        RankTypeFactory.create(type=type)


def init_novel_type():
    """novel_typeの初期データ."""
    for code, name in ((1, "連載"), (2, "短編")):
        NovelTypeFactory.create(code=code, name=name)


def init_biggenre():
    """biggenreの初期データ."""
    for code, name in (
        (0, "未選択"),
        (1, "恋愛"),
        (2, "ファンタジー"),
        (3, "文芸"),
        (4, "SF"),
        (99, "その他"),
        (98, "ノンジャンル"),
    ):
        BigGenreFactory.create(code=code, name=name)


def init_genre():
    """genreの初期データ."""
    for code, name in (
        (0, "未選択〔未選択〕"),
        (101, "異世界〔恋愛〕"),
        (102, "現実世界〔恋愛〕"),
        (201, "ハイファンタジー〔ファンタジー〕"),
        (202, "ローファンタジー〔ファンタジー〕"),
        (301, "純文学〔文芸〕"),
        (302, "ヒューマンドラマ〔文芸〕"),
        (303, "歴史〔文芸〕"),
        (304, "推理〔文芸〕"),
        (305, "ホラー〔文芸〕"),
        (306, "アクション〔文芸〕"),
        (307, "コメディー〔文芸〕"),
        (401, "VRゲーム〔SF〕"),
        (402, "宇宙〔SF〕"),
        (403, "空想科学〔SF〕"),
        (404, "パニック〔SF〕"),
        (9901, "童話〔その他〕"),
        (9902, "詩〔その他〕"),
        (9903, "エッセイ〔その他〕"),
        (9904, "リプレイ〔その他〕"),
        (9999, "その他〔その他〕"),
        (9801, "ノンジャンル〔ノンジャンル〕"),
    ):
        GenreFactory.create(code=code, name=name)


def init_biggenre_genre():
    """biggenre_genreの初期データ."""
    for biggenre_code, genre_code in (
        (0, 0),
        (1, 101),
        (1, 102),
        (2, 201),
        (2, 202),
        (3, 301),
        (3, 302),
        (3, 303),
        (3, 304),
        (3, 305),
        (3, 306),
        (3, 307),
        (4, 401),
        (4, 402),
        (4, 403),
        (4, 404),
        (99, 9901),
        (99, 9902),
        (99, 9903),
        (99, 9904),
        (99, 9999),
        (98, 9801),
    ):
        BigGenreGenreFactory.create(
            biggenre_code=biggenre_code, genre_code=genre_code
        )


def init_db(db):
    """テスト用DBの初期設定."""
    # Factoryの初期設定
    factories = (
        RankTypeFactory,
        RankFactory,
        NcodeMappingFactory,
        NovelTypeFactory,
        BigGenreFactory,
        GenreFactory,
        KeywordFactory,
        AuthorFactory,
        NovelFactory,
        NovelKeywordsFactory,
        BigGenreGenreFactory,
    )
    for factory in factories:
        factory._meta.sqlalchemy_session = db

    # 初期データ
    init_rank_type()
    init_novel_type()
    init_biggenre()
    init_genre()
    init_biggenre_genre()


@pytest.fixture
def db(postgresql_fixture):
    """テスト用DBセッションをSetupするFixture."""
    url = URL.create(
        drivername="postgresql",
        username=postgresql_fixture.info.user,
        password=postgresql_fixture.info.password,
        host=postgresql_fixture.info.host,
        database=postgresql_fixture.info.dbname,
        port=postgresql_fixture.info.port,
    )

    # engineを作成
    engine = create_engine(url, echo=False, poolclass=NullPool)

    # SQLAlchemyで定義しているテーブルを全て作成する
    Base.metadata.create_all(engine)
    SessionFactory = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )

    # Sessionを生成
    db: Session = None
    try:
        db = SessionFactory()
        init_db(db)
        yield db
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()
