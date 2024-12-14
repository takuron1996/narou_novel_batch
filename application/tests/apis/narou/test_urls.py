"""なろうランキングのURL関連のテスト."""

import pytest

from apis.narou.type import OutType, RankType
from apis.narou.urls import NarouRankURLBuilder


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
