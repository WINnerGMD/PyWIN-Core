from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from .. database import Base


class MessagesModel(Base):
    __tablename__ = "messages"

    id = Column(Integer, autoincrement=True, primary_key=True)
    authorID = Column(Integer)
    recipientID = Column(Integer)
    subject = Column(Text)
    body = Column(Text)
