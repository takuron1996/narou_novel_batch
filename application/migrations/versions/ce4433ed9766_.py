"""novelテーブルの作成

Revision ID: ce4433ed9766
Revises: cfcb3ff9d4c9
Create Date: 2024-12-17 05:41:49.753534

このマイグレーションでは、novelテーブルを作成します。
- 主キー: `id`（UUID形式）
- 外部キー:
  - `author_id` → `author`テーブル
  - `biggenre_code` → `biggenre`テーブル
  - `genre_code` → `genre`テーブル
  - `id` → `ncode_mapping`テーブル
  - `novel_type_id` → `novel_type`テーブル
- その他のカラム:
  - 作品名、ジャンル情報、R15、ボーイズラブ、ガールズラブ、残酷描写、異世界転生・転移の有無を示すフラグを含む。
"""


from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ce4433ed9766"
down_revision: Union[str, None] = "cfcb3ff9d4c9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "novel",
        sa.Column("id", sa.UUID(), nullable=False, comment="ID"),
        sa.Column("author_id", sa.UUID(), nullable=False, comment="作者のID"),
        sa.Column(
            "title", sa.String(length=128), nullable=False, comment="作品名"
        ),
        sa.Column(
            "biggenre_code",
            sa.Integer(),
            nullable=False,
            comment="大ジャンルのコード",
        ),
        sa.Column(
            "genre_code",
            sa.Integer(),
            nullable=False,
            comment="ジャンルのコード",
        ),
        sa.Column(
            "novel_type_id",
            sa.Integer(),
            nullable=False,
            comment="ノベルの形式のコード",
        ),
        sa.Column(
            "isr15",
            sa.Boolean(),
            nullable=False,
            comment="「R15」が含まれるかどうか",
        ),
        sa.Column(
            "isbl",
            sa.Boolean(),
            nullable=False,
            comment="「ボーイズラブ」が含まれるかどうか",
        ),
        sa.Column(
            "isgl",
            sa.Boolean(),
            nullable=False,
            comment="「ガールズラブ」が含まれるかどうか",
        ),
        sa.Column(
            "iszankoku",
            sa.Boolean(),
            nullable=False,
            comment="「残酷な描写あり」が含まれるかどうか",
        ),
        sa.Column(
            "istensei",
            sa.Boolean(),
            nullable=False,
            comment="「異世界転生」が含まれるかどうか",
        ),
        sa.Column(
            "istenni",
            sa.Boolean(),
            nullable=False,
            comment="「異世界転移」が含まれるかどうか",
        ),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["author.author_id"],
        ),
        sa.ForeignKeyConstraint(
            ["biggenre_code"],
            ["biggenre.code"],
        ),
        sa.ForeignKeyConstraint(
            ["genre_code"],
            ["genre.code"],
        ),
        sa.ForeignKeyConstraint(
            ["id"],
            ["ncode_mapping.id"],
        ),
        sa.ForeignKeyConstraint(
            ["novel_type_id"],
            ["novel_type.code"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("novel")
    # ### end Alembic commands ###
