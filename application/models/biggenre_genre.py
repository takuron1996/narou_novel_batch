"""biggenre_genreテーブル."""

from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint

from models.base import Base
from models.biggenre import BigGenre
from models.genre import Genre


class BigGenreGenre(Base):
    """大ジャンルとジャンルの中間テーブル."""

    __tablename__ = "biggenre_genre"

    biggenre_code = Column(
        Integer, ForeignKey(BigGenre.code), primary_key=True, nullable=False
    )
    genre_code = Column(
        Integer, ForeignKey(Genre.code), primary_key=True, nullable=False
    )

    # 複合主キーの設定
    __table_args__ = (
        PrimaryKeyConstraint(
            "biggenre_code", "genre_code", name="pk_biggenre_code_genre_code"
        ),
    )
