from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    JSON,
)

from .. database import Base


class RolesModel(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    color = Column(String(255))
    BadgeID = Column(Integer)
    typeMod = Column(Integer)
    rateLevels = Column(Boolean, default=False)
    regular = Column(JSON, default={"downloadLevel": 1, "uploadLevel": 1})

    def __repr__(self):
        return str(
            {
                "id": self.id,
                "color": self.color,
                "badgeID": self.BadgeID,
                "typeMod": self.typeMod,
                "rateLevels": self.rateLevels,
            }
        )
