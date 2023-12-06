from sqlalchemy import (
    Column,
    Integer,
    DateTime
)
from sqlalchemy.sql import func
from database import Base


class FeaturedLevelsModel(Base):
    __tablename__ = "dwlevels"

    id = Column(Integer, autoincrement=True, primary_key=True)
    featuredTime = Column(DateTime(timezone=True), server_default=func.now())
    onTime = Column(DateTime(timezone=True))
    levelid = Column(Integer)
    type = Column(Integer)


    def __repr__(self):
        return str({
            "id": self.id,
            "time": self.time,
            "levelid": self.levelid,
            "type": self.type
        }
        )