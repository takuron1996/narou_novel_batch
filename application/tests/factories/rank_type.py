"""rank_typeのファクトリー関連."""
import factory

from models.rank_type import RankType


class RankTypeFactory(factory.alchemy.SQLAlchemyModelFactory):
    """RankTypeモデルのファクトリー."""

    class Meta:
        """メタデータ."""
        model = RankType  # 対象のモデルを指定
        sqlalchemy_session = None  # セッションを初期化
        sqlalchemy_session_persistence = "commit"  # データをコミットする

    type = factory.Iterator(
        ["d", "w", "m", "q"]
    )  # 日間、週間、月間、四半期のいずれか
    period = factory.LazyAttribute(
        lambda obj: {"d": "日間", "w": "週間", "m": "月間", "q": "四半期"}.get(
            obj.type, "日間"
        )
    )  # `type` に応じて日本語表記を設定
