from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,JSON,Text
from sqlalchemy.orm import relationship

from database import Base
from dataclasses import dataclass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    userName = Column(String(255), unique=True)
    mail = Column(String(255), unique=True)
    role = Column(Integer)
    passhash = Column(String(255))
    verified= Column(Boolean, default=False)
    stars = Column(Integer, default=0)
    diamonds = Column(Integer, default=0)
    coins = Column(Integer, default=0)
    usr_coins = Column(Integer, default=0)
    demons = Column(Integer, default=0)
    cp = Column(Integer, default=0)
    iconkits = Column(JSON, default={"color1": 0, "color2": 3, "accBall": 1, "accBird": 1, "accDart": 1, "accGlow": 0, "accIcon": 1, "accShip": 1, "accRobot": 1, "accSpider": 1, "accExplosion": 1})
    networks = Column(JSON)
    def __repr__(self):
        shprot = {"id": self.id, 
                  "userName": self.userName,
                  "mail": self.mail,
                  "role": self.role,
                  "passhash": self.passhash,
                  "verified":self.verified,
                  "stats": {
                      "stars": self.stars,
                      "diamonds": self.diamonds,
                      "coins": self.coins,
                      "usr_coins": self.usr_coins,
                      "demons": self.demons,
                      "cp": self.cp
                      }
                      
                      }

        return str(shprot)
    
class level(Base):
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
    AudioTrack =  Column(Integer)
    lenght =  Column(Integer)
    stars =  Column(Integer, default=0)
    difficulty =  Column(Integer, default=0)
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
    update_date = Column(Integer , default=0)
    LevelString = Column(Text)


    def __repr__(self):
        return str({
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
            "lenght": self.len,
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
            "LevelString": self.LevelString

        })
    

class Comments(Base):
    __tablename__ = "comments"



    id = Column(Integer, primary_key=True, autoincrement=True)
    authorId = Column(Integer)
    authorName = Column(String(255))
    levelID = Column(Integer, nullable=False)
    content = Column(Text)
    likes = Column(Integer , default=0)
    progress = Column(Integer)
    is_spam = Column(Boolean, default=False)


    def __repr__(self):
        return str({
            "id": self.id,
            "authorId": self.id,
            "content": self.content,
            "likes": self.likes,
            "progress": self.progress,
            "is_spam": self.is_spam
        })




class posts(Base):
    __tablename__ = "post"

    id = Column(Integer, autoincrement=True, primary_key=True)
    accountID = Column(Integer)
    content = Column(Text)

