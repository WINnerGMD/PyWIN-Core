from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    String,
    DateTime,
    func,

)

from .. database import Base


class ListModel(Base):
    __tablename__ = "lists"
    update_date = Column(DateTime(timezone=True), server_default=func.now())
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    desc = Column(String(255))
    version = Column(String(255))
    authorID = Column(Integer)
    authorName = Column(String(255))
    gameVersion = Column(Integer)
    levels = Column(String(60))
    likes = Column(Integer, default=0)
    downloads = Column(Integer, default=0)
    difficultyIcon = Column(Integer, default=0)
    is_feature = Column(Boolean)
