from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
)

from .. database import Base


class CommentsModel(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    authorId = Column(Integer)
    authorName = Column(String(255))
    levelID = Column(Integer, nullable=False)
    content = Column(Text)
    likes = Column(Integer, default=0)
    progress = Column(Integer)
    is_spam = Column(Integer, default=False)

    def __repr__(self):
        return str(
            {
                "id": self.id,
                "authorId": self.id,
                "content": self.content,
                "likes": self.likes,
                "progress": self.progress,
                "is_spam": self.is_spam,
            }
        )
