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
    name = Column(String(255))
    author = Column(String(255))
    link = Column(Text)
    size = Column(Float)
