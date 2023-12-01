from sqlalchemy import (
    Column,
    Integer,
    DateTime,
)
from sqlalchemy.sql import func

from database import Base


class ChestsModel(Base):
    __tablename__ = "Chests"

    id = Column(Integer, autoincrement=True, primary_key=True)
    time = Column(DateTime(timezone=True), server_default=func.now())
    userID = Column(Integer)
    type = Column(Integer)
    orbs = Column(Integer)
    diamonds = Column(Integer)
    fire_shards = Column(Integer)
    ice_shards = Column(Integer)
    poison_shards = Column(Integer)
    shadow_shards = Column(Integer)
    lava_shards = Column(Integer)

