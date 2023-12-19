from sqlalchemy import (
    Column,
    Integer,
    String,
)

from database import Base


class ActionsModel(Base):
    __tablename__ = "actions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    actionName = Column(String(255))
    accountID = Column(Integer)
    value = Column(Integer)
    level = Column(Integer)
    data = Column(String(255))

    def __repr__(self):
        return str(
            {
                "id": self.id,
                "actionName": self.actionName,
                "accountID": self.accountID,
                "value": self.value,
                "level": self.level,
                "data": self.data,
            }
        )
