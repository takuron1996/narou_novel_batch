"""小説情報取得バッチのDB関連のテスト."""

import pytest

from models.author import Author, get_author_id
from models.keyword import Keyword, get_keyword_id
from models.novel import Novel
from repository.get_novel_data_repository import (
    get_target_novel_data,
    insert_author,
    insert_keyword,
    insert_novel,
)
from tests.factories.author import AuthorFactory
from tests.factories.keyword import KeywordFactory
from tests.factories.ncode_mapping import NcodeMappingFactory
from tests.factories.novel import NovelFactory


@pytest.fixture
def novel_with_ncode_mapping():
    """novelテーブルに格納されているデータと紐付くncode_mappingのデータ."""
    return NcodeMappingFactory.create(ncode="N1121JW")


@pytest.fixture
def novel_without_ncode_mapping():
    """novelテーブルに格納されているデータと紐付かないncode_mappingのデータ."""
    return NcodeMappingFactory.create(ncode="N0563JW")


@pytest.fixture
def novel(novel_with_ncode_mapping):
    """novelデータ."""
    return NovelFactory.create(
        id=novel_with_ncode_mapping.id, author_id=AuthorFactory().author_id
    )


@pytest.fixture
def keyword_id():
    """キーワードのID."""
    return get_keyword_id()


@pytest.fixture
def insert_keyword_list(keyword_id):
    """登録したいキーワードのデータ."""
    return [
        {"keyword_id": f"{keyword_id[:-1]}1", "name": "女主人公"},
        {"keyword_id": f"{keyword_id[:-1]}2", "name": "R15"},
        {"keyword_id": f"{keyword_id[:-1]}3", "name": "異世界転生"},
        {"keyword_id": f"{keyword_id[:-1]}4", "name": "魔女"},
        {"keyword_id": f"{keyword_id[:-1]}5", "name": "R18"},
        {"keyword_id": f"{keyword_id[:-1]}6", "name": "男主人公"},
    ]


@pytest.fixture
def userid():
    """作者のID作者のユーザーID(数値)."""
    return 1877427


@pytest.fixture
def author_id():
    """作者のID."""
    return get_author_id()


@pytest.fixture
def insert_author_list(userid, author_id):
    """登録したい作者のデータ."""
    return [
        {"userid": userid, "writer": "aaa", "author_id": f"{author_id[:-1]}1"},
        {
            "userid": userid + 1,
            "writer": "bbb",
            "author_id": f"{author_id[:-1]}2",
        },
        {
            "userid": userid + 2,
            "writer": "ccc",
            "author_id": f"{author_id[:-1]}3",
        },
    ]


@pytest.fixture
def prepare_author_list(userid):
    """準備用のauthor."""
    return [
        AuthorFactory.create(userid=userid, writer="aaa"),
        AuthorFactory.create(userid=userid + 1, writer="bbb"),
        AuthorFactory.create(userid=userid + 2, writer="ccc"),
    ]


@pytest.fixture
def insert_novel_list(
    novel_with_ncode_mapping, novel_without_ncode_mapping, prepare_author_list
):
    """登録したい小説のデータ."""
    return [
        {
            "id": novel_with_ncode_mapping.id,
            "title": "前世は魔女でした！",
            "userid": prepare_author_list[0].userid,
            "biggenre_code": 1,
            "genre_code": 101,
            "novel_type_id": 1,
            "isr15": True,
            "isbl": True,
            "isgl": True,
            "iszankoku": True,
            "istensei": True,
            "istenni": True,
        },
        {
            "id": novel_without_ncode_mapping.id,
            "title": "次の婚約者は人の気持ちのわからないサイコパスです",
            "userid": prepare_author_list[1].userid,
            "biggenre_code": 2,
            "genre_code": 201,
            "novel_type_id": 2,
            "isr15": False,
            "isbl": False,
            "isgl": False,
            "iszankoku": False,
            "istensei": False,
            "istenni": False,
        },
    ]


# get_target_novel_data関連
def test_get_target_novel_data(db, novel_without_ncode_mapping, novel):
    """テスト."""
    results = get_target_novel_data(db)
    assert len(results) == 1
    assert results[0].get("id") == novel_without_ncode_mapping.id
    assert results[0].get("ncode") == novel_without_ncode_mapping.ncode


def test_get_target_novel_data_empty(db, novel):
    """取得したデータが空の場合のテスト."""
    results = get_target_novel_data(db)
    assert results == []


# insert_keyword関連
def test_insert_keyword(db, insert_keyword_list):
    """正常系のテスト."""
    insert_keyword(db, insert_keyword_list)
    results = db.query(Keyword).order_by(Keyword.keyword_id).all()

    assert len(results) == 6
    assert results[0].keyword_id == insert_keyword_list[0].get("keyword_id")
    assert results[0].name == insert_keyword_list[0].get("name")
    assert results[1].keyword_id == insert_keyword_list[1].get("keyword_id")
    assert results[1].name == insert_keyword_list[1].get("name")
    assert results[2].keyword_id == insert_keyword_list[2].get("keyword_id")
    assert results[2].name == insert_keyword_list[2].get("name")
    assert results[3].keyword_id == insert_keyword_list[3].get("keyword_id")
    assert results[3].name == insert_keyword_list[3].get("name")
    assert results[4].keyword_id == insert_keyword_list[4].get("keyword_id")
    assert results[4].name == insert_keyword_list[4].get("name")
    assert results[5].keyword_id == insert_keyword_list[5].get("keyword_id")
    assert results[5].name == insert_keyword_list[5].get("name")


def test_duplicat_insert_keyword(db, insert_keyword_list, keyword_id):
    """重複している場合のテスト."""
    # 事前にデータを作成
    insert_keyword_id = f"{keyword_id[:-1]}9"
    KeywordFactory.create(
        keyword_id=insert_keyword_id, name=insert_keyword_list[0].get("name")
    )

    insert_keyword(db, insert_keyword_list)
    results = db.query(Keyword).order_by(Keyword.keyword_id).all()
    assert len(results) == 6
    assert results[0].keyword_id == insert_keyword_list[1].get("keyword_id")
    assert results[0].name == insert_keyword_list[1].get("name")
    assert results[1].keyword_id == insert_keyword_list[2].get("keyword_id")
    assert results[1].name == insert_keyword_list[2].get("name")
    assert results[2].keyword_id == insert_keyword_list[3].get("keyword_id")
    assert results[2].name == insert_keyword_list[3].get("name")
    assert results[3].keyword_id == insert_keyword_list[4].get("keyword_id")
    assert results[3].name == insert_keyword_list[4].get("name")
    assert results[4].keyword_id == insert_keyword_list[5].get("keyword_id")
    assert results[4].name == insert_keyword_list[5].get("name")
    assert results[5].keyword_id == insert_keyword_id
    assert results[5].name == insert_keyword_list[0].get("name")


# insert_author関連
def test_insert_author(db, insert_author_list):
    """正常系のテスト."""
    insert_author(db, insert_author_list)
    results = db.query(Author).order_by(Author.userid).all()
    assert len(results) == 3
    assert results[0].author_id == insert_author_list[0].get("author_id")
    assert results[0].userid == insert_author_list[0].get("userid")
    assert results[0].writer == insert_author_list[0].get("writer")
    assert results[1].author_id == insert_author_list[1].get("author_id")
    assert results[1].userid == insert_author_list[1].get("userid")
    assert results[1].writer == insert_author_list[1].get("writer")
    assert results[2].author_id == insert_author_list[2].get("author_id")
    assert results[2].userid == insert_author_list[2].get("userid")
    assert results[2].writer == insert_author_list[2].get("writer")


def test_duplicat_insert_author(db, insert_author_list, userid, author_id):
    """重複している場合のテスト."""
    # 事前にデータを作成
    insert_writer = "hogehoge"
    insert_author_id = f"{author_id[:-1]}9"
    AuthorFactory.create(
        userid=userid, author_id=insert_author_id, writer=insert_writer
    )

    insert_author(db, insert_author_list)
    results = db.query(Author).order_by(Author.userid).all()

    assert len(results) == 3
    assert results[0].author_id == insert_author_id
    assert results[0].userid == insert_author_list[0].get("userid")
    assert results[0].writer == insert_author_list[0].get("writer")
    assert results[1].author_id == insert_author_list[1].get("author_id")
    assert results[1].userid == insert_author_list[1].get("userid")
    assert results[1].writer == insert_author_list[1].get("writer")
    assert results[2].author_id == insert_author_list[2].get("author_id")
    assert results[2].userid == insert_author_list[2].get("userid")
    assert results[2].writer == insert_author_list[2].get("writer")


# insert_novel関連
def test_insert_novel(db, insert_novel_list, prepare_author_list):
    """正常系のテスト."""
    insert_novel(db, insert_novel_list)
    results = db.query(Novel).order_by(Novel.biggenre_code).all()

    assert len(results) == 2
    assert results[0].id == insert_novel_list[0].get("id")
    assert results[0].author_id == prepare_author_list[0].author_id
    assert results[0].title == insert_novel_list[0].get("title")
    assert results[0].biggenre_code == insert_novel_list[0].get("biggenre_code")
    assert results[0].genre_code == insert_novel_list[0].get("genre_code")
    assert results[0].novel_type_id == insert_novel_list[0].get("novel_type_id")
    assert results[0].isr15
    assert results[0].isbl
    assert results[0].isgl
    assert results[0].iszankoku
    assert results[0].istensei
    assert results[0].istenni

    assert results[1].id == insert_novel_list[1].get("id")
    assert results[1].author_id == prepare_author_list[1].author_id
    assert results[1].title == insert_novel_list[1].get("title")
    assert results[1].biggenre_code == insert_novel_list[1].get("biggenre_code")
    assert results[1].genre_code == insert_novel_list[1].get("genre_code")
    assert results[1].novel_type_id == insert_novel_list[1].get("novel_type_id")
    assert not results[1].isr15
    assert not results[1].isbl
    assert not results[1].isgl
    assert not results[1].iszankoku
    assert not results[1].istensei
    assert not results[1].istenni


def test_duplicat_insert_novel(
    db, insert_novel_list, prepare_author_list, novel_with_ncode_mapping
):
    """重複している場合のテスト."""
    # 事前にデータを作成
    NovelFactory.create(
        id=novel_with_ncode_mapping.id,
        author_id=prepare_author_list[2].author_id,
    )

    insert_novel(db, insert_novel_list)
    results = db.query(Novel).order_by(Novel.biggenre_code).all()

    assert len(results) == 2
    assert results[0].id == insert_novel_list[0].get("id")
    assert results[0].author_id == prepare_author_list[0].author_id
    assert results[0].title == insert_novel_list[0].get("title")
    assert results[0].biggenre_code == insert_novel_list[0].get("biggenre_code")
    assert results[0].genre_code == insert_novel_list[0].get("genre_code")
    assert results[0].novel_type_id == insert_novel_list[0].get("novel_type_id")
    assert results[0].isr15
    assert results[0].isbl
    assert results[0].isgl
    assert results[0].iszankoku
    assert results[0].istensei
    assert results[0].istenni

    assert results[1].id == insert_novel_list[1].get("id")
    assert results[1].author_id == prepare_author_list[1].author_id
    assert results[1].title == insert_novel_list[1].get("title")
    assert results[1].biggenre_code == insert_novel_list[1].get("biggenre_code")
    assert results[1].genre_code == insert_novel_list[1].get("genre_code")
    assert results[1].novel_type_id == insert_novel_list[1].get("novel_type_id")
    assert not results[1].isr15
    assert not results[1].isbl
    assert not results[1].isgl
    assert not results[1].iszankoku
    assert not results[1].istensei
    assert not results[1].istenni
