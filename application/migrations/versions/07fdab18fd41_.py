"""rankテーブルの主キー変更およびrank_typeテーブルの追加

Revision ID: 07fdab18fd41
Revises: 08f7d1c486c3
Create Date: 2024-12-11 09:46:16.957015

このマイグレーションでは、rankテーブルの主キーを変更し、新たにrank_typeテーブルを作成します。
rankテーブルにはrank_type列を追加し、rank_typeテーブルとの外部キー制約を設定します。
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "07fdab18fd41"
down_revision: Union[str, None] = "08f7d1c486c3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # 既存の主キー制約を削除
    op.drop_constraint("pk_rank", "rank", type_="primary")

    # rank_typeテーブルを作成
    op.create_table(
        "rank_type",
        sa.Column("type", sa.String(length=1), nullable=False),
        sa.Column("period", sa.String(length=10), nullable=False),
        sa.PrimaryKeyConstraint("type"),
    )
    # rankテーブルにrank_type列を追加
    op.add_column(
        "rank", sa.Column("rank_type", sa.String(length=1), nullable=False)
    )
    # 外部キー制約を追加
    op.create_foreign_key(None, "rank", "rank_type", ["rank_type"], ["type"])

    # 新しい複合主キーを作成
    op.create_primary_key(
        "pk_rank",  # 制約名
        "rank",  # テーブル名
        ["id", "rank", "rank_date", "rank_type"],  # 主キー列
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # 新しい複合主キー制約を削除
    op.drop_constraint("pk_rank", "rank", type_="primary")
    # 外部キー制約を削除
    op.drop_constraint(None, "rank", type_="foreignkey")
    # rank_type列を削除
    op.drop_column("rank", "rank_type")
    # rank_typeテーブルを削除
    op.drop_table("rank_type")
    # 元の主キー制約を再作成
    op.create_primary_key(
        "pk_rank", "rank", ["id", "rank", "rank_date"]  # 元の主キー列
    )
    # ### end Alembic commands ###
