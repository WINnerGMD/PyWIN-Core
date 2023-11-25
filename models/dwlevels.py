from sqlalchemy import (
    Column,
    Integer,
)

from database import Base


class FeaturedLevelsModel(Base):
    __tablename__ = "dwlevels"

    id = Column(Integer, autoincrement=True, primary_key=True)
    type = Column(Integer)
