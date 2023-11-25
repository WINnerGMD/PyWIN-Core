from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
)

from database import Base


class LevelsModel(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    desc = Column(Text)
    version = Column(Integer)
    authorID = Column(Integer)
    authorName = Column(String(255))
    gameVersion = Column(Integer)
    likes = Column(Integer, default=0)
    downloads = Column(Integer, default=0)
    AudioTrack = Column(Integer)
    lenght = Column(Integer)
    stars = Column(Integer, default=0)
    difficulty = Column(Integer, default=0)
    coins = Column(Integer)
    user_coins = Column(Integer)
    rate = Column(Integer, default=0)
    original = Column(Integer)
    two_players = Column(Integer)
    song_id = Column(Integer)
    is_ldm = Column(Integer)
    objects = Column(Integer)
    password = Column(Integer)
    upload_date = Column(String(255))
    update_date = Column(Integer, default=0)
    LevelString = Column(Text)

    def __repr__(self):
        return str(
            {
                "id": self.id,
                "name": self.id,
                "desc": self.desc,
                "version": self.version,
                "authorID": self.authorID,
                "AuthorName": self.authorName,
                "gameVersion": self.gameVersion,
                "likes": self.likes,
                "downloads": self.downloads,
                "AudioTrack": self.AudioTrack,
                "song_id": self.song_id,
                "lenght": self.lenght,
                "stars": self.stars,
                "coins": self.coins,
                "difficulty": self.difficulty,
                "user_coins": self.user_coins,
                "rate": self.rate,
                "original": self.rate,
                "two_players": self.two_players,
                "is_ldm": self.is_ldm,
                "objects": self.objects,
                "password": self.password,
                "LevelString": self.LevelString,
            }
        )
