"""なろうランキングの挿入関連のテスト."""

import uuid

import pytest

from apis.narou.narou_data import NarouRankData
from common.datetime_util import jst_strptime
from models.ncode_mapping import NcodeMapping
from models.rank import Rank
from repository.daily_get_ranking_repository import ranking_insert


@pytest.fixture
def initial_narou_rank_data():
    """初期データのNarouRankDataリストを返すフィクスチャ."""
    return [
        NarouRankData(
            id=uuid.uuid4(),
            ncode="ncode1",
            rank=1,
            rank_date="20241211",
            pt=101,
            rank_type="d",
        ),
        NarouRankData(
            id=uuid.uuid4(),
            ncode="ncode2",
            rank=2,
            rank_date="20241211",
            pt=100,
            rank_type="d",
        ),
    ]


@pytest.fixture
def duplicate_narou_rank_data():
    """初期データのNarouRankDataリストを返すフィクスチャ."""
    return [
        NarouRankData(
            id=uuid.uuid4(),
            ncode="ncode1",
            rank=1,
            rank_date="20241212",
            pt=99,
            rank_type="d",
        ),  # ncode1が重複
        NarouRankData(
            id=uuid.uuid4(),
            ncode="ncode3",
            rank=2,
            rank_date="20241212",
            pt=98,
            rank_type="d",
        ),
    ]


def test_insert_ncode_mapping(db, initial_narou_rank_data):
    """ncode_mappingへのデータ挿入のテスト."""
    ranking_insert(db, initial_narou_rank_data)

    results = db.query(NcodeMapping).order_by(NcodeMapping.ncode).all()

    assert len(results) == 2
    assert results[0].ncode == initial_narou_rank_data[0].ncode
    assert results[0].id == initial_narou_rank_data[0].id
    assert results[1].ncode == initial_narou_rank_data[1].ncode
    assert results[1].id == initial_narou_rank_data[1].id


def test_duplicate_ncode_handling(
    db, initial_narou_rank_data, duplicate_narou_rank_data
):
    """重複したncodeの処理テスト."""
    # 最初のデータ挿入
    ranking_insert(db, initial_narou_rank_data)

    # 重複するncodeを含む新しいデータを挿入
    ranking_insert(db, duplicate_narou_rank_data)

    results = db.query(NcodeMapping).order_by(NcodeMapping.ncode).all()

    # ncode1が重複しているが、最初に登録されたidのデータが保持されていることを確認
    assert len(results) == 3
    assert results[0].ncode == initial_narou_rank_data[0].ncode
    assert results[0].id == initial_narou_rank_data[0].id
    assert results[1].ncode == initial_narou_rank_data[1].ncode
    assert results[1].id == initial_narou_rank_data[1].id
    assert results[2].ncode == duplicate_narou_rank_data[1].ncode
    assert results[2].id == duplicate_narou_rank_data[1].id


def test_rank_table_insertion(db, initial_narou_rank_data):
    """rankテーブルへのデータ挿入テスト."""
    # 初期データを挿入
    ranking_insert(db, initial_narou_rank_data)

    # rankテーブルのデータを取得
    rank_results = db.query(Rank).order_by(Rank.rank_date, Rank.rank).all()

    # rankテーブルの挿入内容を確認
    assert len(rank_results) == 2
    assert rank_results[0].id == initial_narou_rank_data[0].id
    assert rank_results[0].rank == initial_narou_rank_data[0].rank
    assert rank_results[0].rank_date == jst_strptime("20241211").date()
    assert rank_results[0].rank_type == initial_narou_rank_data[0].rank_type
    assert rank_results[1].id == initial_narou_rank_data[1].id
    assert rank_results[1].rank == initial_narou_rank_data[1].rank
    assert rank_results[1].rank_date == jst_strptime("20241211").date()
    assert rank_results[1].rank_type == initial_narou_rank_data[1].rank_type


def test_rank_table_with_duplicate_ncode(
    db, initial_narou_rank_data, duplicate_narou_rank_data
):
    """rankテーブルに重複したncodeが含まれていても全て取り込まれていることのテスト."""
    # 最初のデータ挿入
    ranking_insert(db, initial_narou_rank_data)

    # 重複データ挿入
    ranking_insert(db, duplicate_narou_rank_data)

    # rankテーブルのデータを取得
    rank_results = db.query(Rank).order_by(Rank.rank_date, Rank.rank).all()

    # rankテーブルの挿入内容を確認
    assert len(rank_results) == 4
    assert rank_results[0].id == initial_narou_rank_data[0].id
    assert rank_results[0].rank == initial_narou_rank_data[0].rank
    assert rank_results[0].rank_date == jst_strptime("20241211").date()
    assert rank_results[0].rank_type == "d"

    assert rank_results[1].id == initial_narou_rank_data[1].id
    assert rank_results[1].rank == initial_narou_rank_data[1].rank
    assert rank_results[1].rank_date == jst_strptime("20241211").date()
    assert rank_results[1].rank_type == initial_narou_rank_data[1].rank_type

    # 重複ncodeでもrankに追加される
    assert rank_results[2].id == initial_narou_rank_data[0].id
    assert rank_results[2].rank == duplicate_narou_rank_data[0].rank
    assert rank_results[2].rank_date == jst_strptime("20241212").date()
    assert rank_results[2].rank_type == duplicate_narou_rank_data[0].rank_type

    assert rank_results[3].id == duplicate_narou_rank_data[1].id
    assert rank_results[3].rank == duplicate_narou_rank_data[1].rank
    assert rank_results[3].rank_date == jst_strptime("20241212").date()
    assert rank_results[3].rank_type == duplicate_narou_rank_data[1].rank_type
