from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sql import models
from objects.schemas import UploadLevel,GetLevel
import json
from services.user import UserService
from datetime import datetime, timedelta

class LevelService:
    


    def upload_level(self, db: Session,data: UploadLevel):
        AuthorObj = UserService().get_user_byid(db=db, id=data.accountID)
        if AuthorObj != None:

            db_lvl = models.level(name=data.levelName,
                                #   desc = data.levelDesc,
                                  version= data.levelVersion,
                                  authorID = data.accountID,
                                  authorName = AuthorObj.userName, 
                                  gameVersion = data.gameVersion, 
                                  AudioTrack=data.audioTrack,
                                  lenght = data.levelLength, 
                                  coins = data.coins, 
                                  user_coins = 0, 
                                  original=data.original,
                                  two_players = data.twoPlayer, 
                                  song_id = data.songID,
                                  is_ldm = data.ldm, 
                                  password = data.password,
                                  upload_date= datetime.utcnow(),
                                  LevelString = data.levelString
                                   )
            db.add(db_lvl)
            db.commit()
            db.refresh(db_lvl)
    

    def get_levels(self,db: Session,data: GetLevel):
        page = int(data.page) * 5
        difficulty = data.difficulty
        if difficulty == "-1":
            difficulty = 0
        elif difficulty == "-2":
            difficulty = int(data.demonFilter) + 6
        result = (db.query(models.level).filter( models.level.coins > 0 if data.coins == "1" 
                                                 else models.level.coins >= 0 ,

                                                 models.level.lenght >= 0 if data.lenght == "-" 
                                                 else models.level.lenght == data.lenght,
                                                 
                                                 models.level.difficulty >= -3 if data.difficulty == "-" 
                                                 else models.level.difficulty == difficulty,

                                                 )
                                                 )
        if data.type == "2":
            return result.order_by(models.level.likes.desc(), models.level.downloads.desc()).offset(page).limit(5).all()
        elif data.type == "0":
            return result.filter(models.level.name.like(f"%{data.str}%")).order_by(models.level.likes.desc(), models.level.downloads.desc()).offset(page).limit(5).all()
        elif data.type == "5":
            return result.filter(models.level.authorID == data.str).all()
        elif data.type == "6":
            return result.filter(models.level.rate == 1).all()
        elif data.type == "4":
            return result.order_by(models.level.id.desc())
        elif data.type == "16":
            return result.filter(models.level.rate >= 1).all()
        else:
            return result.all()
    


    def get_level_buid(self,db: Session, level_id):
        return db.query(models.level).filter(models.level.id == level_id).first()
