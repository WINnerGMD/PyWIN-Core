from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,

)
from src.helpers.rate import Rate, Difficulty
from src.schemas.levels.model import APILevelSchema, StatsSchema
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class LevelModel(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    desc = Column(String(255))
    version = Column(String(255))
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

    def to_API_model(self) -> APILevelSchema:
        """
        Converter to LevelAPI Scheme.
        Without security data

        Return LevelAPIScheme
        """
        return APILevelSchema(
            id=self.id,
            name=self.name,
            desc=self.desc,
            version=self.version,
            authorID=self.authorID,
            AuthorName=self.authorName,
            gameVersion=self.gameVersion,
            AudioTrack=self.AudioTrack,
            song_id=self.song_id,
            lenght=self.lenght,
            difficulty=Difficulty(self.difficulty).name,
            rate=Rate(self.rate).name,
            original=self.rate,
            two_players=self.two_players,
            is_ldm=self.is_ldm,
            password=self.password,
            LevelString=self.LevelString,
            stats=StatsSchema(
                stars=self.stars,
                coins=self.coins,
                user_coins=self.user_coins,
                objects=self.objects,
                likes=self.likes,
                downloads=self.downloads,
            )
        )
