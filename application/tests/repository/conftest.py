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
from tests.factories.genre import GenreFactory
from tests.factories.keyword import KeywordFactory
from tests.factories.ncode_mapping import NcodeMappingFactory
from tests.factories.novel import NovelFactory
from tests.factories.novel_type import NovelTypeFactory
from tests.factories.rank import RankFactory
from tests.factories.rank_type import RankTypeFactory
from tests.factories.novel_keywords import NovelKeywordsFactory

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
    )
    for factory in factories:
        factory._meta.sqlalchemy_session = db

    # 初期データ
    ## rank_type
    RankTypeFactory.create(type="d")
    RankTypeFactory.create(type="w")
    RankTypeFactory.create(type="m")
    RankTypeFactory.create(type="q")
    ## novel_type
    NovelTypeFactory.create(code=1, name="連載")
    NovelTypeFactory.create(code=2, name="短編")
    ## biggenre
    BigGenreFactory.create(code=0, name="未選択")
    BigGenreFactory.create(code=1, name="恋愛")
    BigGenreFactory.create(code=2, name="ファンタジー")
    BigGenreFactory.create(code=3, name="文芸")
    BigGenreFactory.create(code=4, name="SF")
    BigGenreFactory.create(code=99, name="その他")
    BigGenreFactory.create(code=98, name="ノンジャンル")
    ## genre
    GenreFactory.create(code=0, name="未選択〔未選択〕", biggenre_code=0)
    GenreFactory.create(code=101, name="異世界〔恋愛〕", biggenre_code=1)
    GenreFactory.create(code=102, name="現実世界〔恋愛〕", biggenre_code=1)
    GenreFactory.create(
        code=201, name="ハイファンタジー〔ファンタジー〕", biggenre_code=2
    )
    GenreFactory.create(
        code=202, name="ローファンタジー〔ファンタジー〕", biggenre_code=2
    )
    GenreFactory.create(code=301, name="純文学〔文芸〕", biggenre_code=3)
    GenreFactory.create(
        code=302, name="ヒューマンドラマ〔文芸〕", biggenre_code=3
    )
    GenreFactory.create(code=303, name="歴史〔文芸〕", biggenre_code=3)
    GenreFactory.create(code=304, name="推理〔文芸〕", biggenre_code=3)
    GenreFactory.create(code=305, name="ホラー〔文芸〕", biggenre_code=3)
    GenreFactory.create(code=306, name="アクション〔文芸〕", biggenre_code=3)
    GenreFactory.create(code=307, name="コメディー〔文芸〕", biggenre_code=3)
    GenreFactory.create(code=401, name="VRゲーム〔SF〕", biggenre_code=4)
    GenreFactory.create(code=402, name="宇宙〔SF〕", biggenre_code=4)
    GenreFactory.create(code=403, name="空想科学〔SF〕", biggenre_code=4)
    GenreFactory.create(code=404, name="パニック〔SF〕", biggenre_code=4)
    GenreFactory.create(code=9901, name="童話〔その他〕", biggenre_code=99)
    GenreFactory.create(code=9902, name="詩〔その他〕", biggenre_code=99)
    GenreFactory.create(code=9903, name="エッセイ〔その他〕", biggenre_code=99)
    GenreFactory.create(code=9904, name="リプレイ〔その他〕", biggenre_code=99)
    GenreFactory.create(code=9999, name="その他〔その他〕", biggenre_code=99)
    GenreFactory.create(
        code=9801, name="ノンジャンル〔ノンジャンル〕", biggenre_code=98
    )


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
