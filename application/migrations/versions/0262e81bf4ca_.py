"""empty message

Revision ID: 0262e81bf4ca
Revises: d6c12aa8111c
Create Date: 2024-12-16 15:26:12.044629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0262e81bf4ca'
down_revision: Union[str, None] = 'd6c12aa8111c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('biggenre',
    sa.Column('code', sa.Integer(), nullable=False, comment='大ジャンルのコード'),
    sa.Column('name', sa.String(length=36), nullable=False, comment='大ジャンル名'),
    sa.PrimaryKeyConstraint('code')
    )
    op.create_table('genre',
    sa.Column('code', sa.Integer(), nullable=False, comment='ジャンルのコード'),
    sa.Column('name', sa.String(length=36), nullable=False, comment='ジャンル名'),
    sa.Column('biggenre_code', sa.Integer(), nullable=False, comment='大ジャンルのコード'),
    sa.ForeignKeyConstraint(['biggenre_code'], ['biggenre.code'], ),
    sa.PrimaryKeyConstraint('code')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('genre')
    op.drop_table('biggenre')
    # ### end Alembic commands ###
