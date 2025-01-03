"""なろうランキングのURL関連のテスト."""

import pytest

from apis.narou.type import (
    NarouLimitType,
    NarouOfType,
    NarouOrderType,
    OutType,
    RankType,
)
from apis.narou.urls import NarouRankURLBuilder, NarouURLBuilder


# NarouRankURLBuilder
def test_build_success():
    """正常なパラメータでURLが正しく生成されることをテスト."""
    builder = NarouRankURLBuilder()
    url = (
        builder.set_date("20230501")
        .set_rank_type(RankType.DAILY)
        .set_output_format(OutType.JSON)
        .build()
    )
    expected_url = (
        "https://api.syosetu.com/rank/rankget/?rtype=20230501-d&out=json"
    )
    assert url == expected_url


def test_missing_required_params():
    """必須パラメータが不足している場合のエラーチェック."""
    builder = NarouRankURLBuilder()
    with pytest.raises(
        ValueError, match="必須パラメータが不足しています: DATE, RANK_TYPE"
    ):
        builder.build()


def test_invalid_date_for_rank_type():
    """無効な日付が指定された場合のエラーチェック."""
    builder = NarouRankURLBuilder()

    # ケース1: 週間ランキングに月曜日を指定
    with pytest.raises(
        ValueError,
        match="日付 20231204 はランキングタイプ WEEKLY に対して無効です。",
    ):
        (
            builder.set_date(
                "20231204"
            )  # 月曜日 (週間ランキングは火曜日のみ有効)
            .set_rank_type(RankType.WEEKLY)
            .set_output_format(OutType.JSON)
            .build()
        )

    # ケース2: 月間ランキングに2日を指定
    with pytest.raises(
        ValueError,
        match="日付 20231202 はランキングタイプ MONTHLY に対して無効です。",
    ):
        (
            builder.set_date("20231202")  # 月間ランキングは1日だけ有効
            .set_rank_type(RankType.MONTHLY)
            .set_output_format(OutType.JSON)
            .build()
        )

    # ケース3: 四半期ランキングに2日を指定
    with pytest.raises(
        ValueError,
        match="日付 20231002 はランキングタイプ QUARTERLY に対して無効です。",
    ):
        (
            builder.set_date("20231002")  # 四半期ランキングも1日だけ有効
            .set_rank_type(RankType.QUARTERLY)
            .set_output_format(OutType.JSON)
            .build()
        )

    # ケース4: 日間ランキングに2013年5月1日以前の日付を指定
    with pytest.raises(
        ValueError,
        match="日付 20130430 はランキングタイプ DAILY に対して無効です。",
    ):
        (
            builder.set_date("20130430")  # 境界値: 2013年5月1日より前は無効
            .set_rank_type(RankType.DAILY)
            .set_output_format(OutType.JSON)
            .build()
        )

    # ケース5: 日付形式が不正
    with pytest.raises(
        ValueError,
        match="日付 invalid_date はランキングタイプ DAILY に対して無効です。",
    ):
        (
            builder.set_date("invalid_date")  # 無効な形式
            .set_rank_type(RankType.DAILY)
            .set_output_format(OutType.JSON)
            .build()
        )


def test_default_output_format():
    """デフォルトの出力形式がJSONであることをテスト."""
    builder = NarouRankURLBuilder()
    builder.set_date("20231205").set_rank_type(RankType.DAILY)
    url = builder.build()
    assert "out=json" in url


# NarouURLBuilder
def test_NarouURLBuilder_only_output_format():
    """出力形式のみ設定した場合、他のパラメータが含まれないことを確認."""
    url = NarouURLBuilder().set_output_format(OutType.JSON).build()
    assert "out=json" in url  # 出力形式が含まれる
    assert "ncode=" not in url  # ncodeが含まれない
    assert "of=" not in url  # ofが含まれない
    assert "order=" not in url  # orderが含まれない
    assert "lim=" not in url  # limitが含まれない


def test_NarouURLBuilder_only_ncode():
    """ncodeのみ設定した場合、他のパラメータが含まれないことを確認."""
    url = NarouURLBuilder().set_ncode("N5678").build()
    assert "ncode=N5678" in url  # ncodeが含まれる
    assert "out=" not in url  # 出力形式が含まれない
    assert "of=" not in url  # ofが含まれない
    assert "order=" not in url  # orderが含まれない
    assert "lim=" not in url  # limitが含まれない


def test_NarouURLBuilder_only_of_list():
    """項目リストのみ設定した場合、他のパラメータが含まれないことを確認."""
    url = NarouURLBuilder().set_of_list([NarouOfType.TITLE]).build()
    assert "of=t" in url  # 項目リストが含まれる
    assert "out=" not in url  # 出力形式が含まれない
    assert "ncode=" not in url  # ncodeが含まれない
    assert "order=" not in url  # orderが含まれない
    assert "lim=" not in url  # limitが含まれない


def test_NarouURLBuilder_only_order():
    """出力順序のみ設定した場合、他のパラメータが含まれないことを確認."""
    url = NarouURLBuilder().set_order(NarouOrderType.NEW).build()
    assert "order=new" in url  # 出力順序が含まれる
    assert "out=" not in url  # 出力形式が含まれない
    assert "ncode=" not in url  # ncodeが含まれない
    assert "of=" not in url  # ofが含まれない
    assert "lim=" not in url  # limitが含まれない


def test_NarouURLBuilder_combined_params():
    """複数のパラメータを設定した場合のテスト."""
    url = (
        NarouURLBuilder()
        .set_output_format(OutType.JSON)
        .set_ncode("N1234")
        .set_of_list([NarouOfType.TITLE, NarouOfType.WRITER])
        .set_order(NarouOrderType.NEW)
        .set_limit(NarouLimitType.MAX_FETCH_LIMIT.value)
        .build()
    )
    assert "out=json" in url  # 出力形式が含まれる
    assert "ncode=N1234" in url  # ncodeが含まれる
    assert "of=t-w" in url  # 項目リストが含まれる
    assert "order=new" in url  # 出力順序が含まれる
    assert (
        f"lim={NarouLimitType.MAX_FETCH_LIMIT.value}" in url
    )  # 出力数が含まれる


def test_test_NarouURLBuilder_min_value():
    """limitが最小値の場合のテスト."""
    url = (
        NarouURLBuilder()
        .set_limit(NarouLimitType.MIN_FETCH_LIMIT.value)
        .build()
    )
    assert f"lim={NarouLimitType.MIN_FETCH_LIMIT.value}" in url


def test_test_NarouURLBuilder_less_than_min():
    """limitが最小値未満の場合のテスト."""
    url = (
        NarouURLBuilder()
        .set_limit(NarouLimitType.MIN_FETCH_LIMIT.value - 1)
        .build()
    )
    assert f"lim={NarouLimitType.MIN_FETCH_LIMIT.value}" in url


def test_test_NarouURLBuilder_max():
    """limitが最大値の場合のテスト."""
    url = (
        NarouURLBuilder()
        .set_limit(NarouLimitType.MAX_FETCH_LIMIT.value)
        .build()
    )
    assert f"lim={NarouLimitType.MAX_FETCH_LIMIT.value}" in url


def test_test_NarouURLBuilder_greater_than_500():
    """limitが最大値より大きい場合のテスト."""
    url = (
        NarouURLBuilder()
        .set_limit(NarouLimitType.MAX_FETCH_LIMIT.value + 1)
        .build()
    )
    assert f"lim={NarouLimitType.MAX_FETCH_LIMIT.value}" in url


def test_NarouURLBuilder_no_params():
    """全てのパラメータを指定しない場合."""
    url = NarouURLBuilder().build()
    assert url == "https://api.syosetu.com/novelapi/api/?"
