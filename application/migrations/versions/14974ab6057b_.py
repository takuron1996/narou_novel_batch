"""empty message

Revision ID: 14974ab6057b
Revises: ec45656b488a
Create Date: 2024-12-26 21:44:56.496418

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "14974ab6057b"
down_revision: Union[str, None] = "ec45656b488a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # 外部キー制約を一時的に削除
    op.drop_constraint("novel_author_id_fkey", "novel", type_="foreignkey")
    # authorテーブルのauthor_idを修正
    op.alter_column(
        "author",
        "author_id",
        existing_type=sa.UUID(),
        type_=sa.String(length=42),
        existing_comment="作者のID",
        existing_nullable=False,
    )

    # novelテーブルのauthor_idを修正
    op.alter_column(
        "novel",
        "author_id",
        existing_type=sa.UUID(),
        type_=sa.String(length=42),
        existing_comment="作者のID",
        existing_nullable=False,
    )

    # 外部キー制約を復旧
    op.create_foreign_key(
        "novel_author_id_fkey", "novel", "author", ["author_id"], ["author_id"]
    )


def downgrade() -> None:
    # 外部キー制約を一時的に削除
    op.drop_constraint("novel_author_id_fkey", "novel", type_="foreignkey")

    # authorテーブルのauthor_idを元のUUID型に戻す
    op.alter_column(
        "author",
        "author_id",
        existing_type=sa.String(length=42),
        type_=sa.UUID(),
        existing_comment="作者のID",
        existing_nullable=False,
    )

    # novelテーブルのauthor_idを元のUUID型に戻す
    op.alter_column(
        "novel",
        "author_id",
        existing_type=sa.String(length=42),
        type_=sa.UUID(),
        existing_comment="作者のID",
        existing_nullable=False,
    )

    # 外部キー制約を復旧
    op.create_foreign_key(
        "novel_author_id_fkey", "novel", "author", ["author_id"], ["author_id"]
    )
