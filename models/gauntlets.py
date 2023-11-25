from sqlalchemy import (
    Column,
    Integer,
    String,
)

from database import Base


class GauntletsModel(Base):
    __tablename__ = "gauntlets"

    id = Column(Integer, autoincrement=True, primary_key=True)
    indexpack = Column(Integer)
    levels = Column(String(255))
