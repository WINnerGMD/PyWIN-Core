from sqlalchemy import (
    Column,
    Integer,
    String,
)

from .. database import Base


class MapPacksModel(Base):
    __tablename__ = "mappacks"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255))
    levels = Column(String(255))
    stars = Column(Integer)
    coins = Column(Integer)
    difficulty = Column(Integer)
    text_color = Column(String(255))
    bar_color = Column(String(255))
