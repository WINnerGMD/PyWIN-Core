from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
)

from .. database import Base


class PostsModel(Base):
    __tablename__ = "posts"

    id = Column(Integer, autoincrement=True, primary_key=True)
    accountID = Column(Integer)
    content = Column(Text)
    likes = Column(Integer, default=0)
    percent = Column(Integer, default=0)
    lvllink = Column(Integer, default=0)
    timestamp = Column(String(255), default="0-0-0")

    def __repr__(self):
        return str(
            {
                "id": self.id,
                "accountID": self.accountID,
                "content": self.content,
                "likes": self.likes,
                "percent": self.percent,
                "lvllink": self.lvllink,
                "timestamp": self.timestamp,
            }
        )
