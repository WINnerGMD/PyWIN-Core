from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
)

from database import Base


class SongsModel(Base):
    __tablename__ = "songs"

    id = Column(Integer, autoincrement=True, primary_key=True)
    song_id = Column(Integer)
    name = Column(String(255))
    author = Column(String(255))
    size = Column(Float)
