"""keywordテーブルにnameカラムのユニーク制約を追加

Revision ID: 498a9eaf15d1
Revises: 4b91e6c70ca7
Create Date: 2024-12-17 15:45:25.624094

このマイグレーションでは、keywordテーブルの`name`カラムにユニーク制約を追加します。
これにより、重複するキーワード名の登録を防止します。
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "498a9eaf15d1"
down_revision: Union[str, None] = "4b91e6c70ca7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "keyword", ["name"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "keyword", type_="unique")
    # ### end Alembic commands ###