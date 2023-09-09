from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,insert
from sql import models
from objects.schemas import UploadLevel,GetLevel, DownloadItem
import json
from services.user import UserService
from datetime import datetime, timedelta
from sqlalchemy import Delete, Update
import datetime
from logger import info, error, warning
class LevelService:
    
    @staticmethod
    async def upload_level(db: AsyncSession,data: UploadLevel):
        AuthorObj = await UserService().get_user_byid(db=db, id=data.accountID)
        upload_time = datetime.datetime.utcnow()
        if AuthorObj != None:

            db_lvl = models.Levels(name=data.levelName,
                                  desc = data.levelDesc,
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
                                  upload_date= upload_time,
                                  LevelString = data.levelString
                                   )
            db.add(db_lvl)
            await db.commit()
            await db.refresh(db_lvl)



            logs = models.Events(type='levelUpload',playerID = data.accountID,valueID = db_lvl.id, timestamp = upload_time)
            db.add(logs)
            await db.commit()
            await db.refresh(logs)
            return db_lvl
    @staticmethod
    async def get_levels(db: AsyncSession,data: GetLevel):
        try:
            if data.page != None:
                page = int(data.page) * 10
            difficulty = data.difficulty
            if difficulty == "-1":
                difficulty = 0
            elif difficulty == "-2":
                difficulty = int(data.demonFilter) + 6
            result = (select(models.Levels).filter( models.Levels.coins > 0 if data.coins == "1" 
                                                    else models.Levels.coins >= 0 ,

                                                    models.Levels.lenght >= 0 if data.lenght == "-" 
                                                    else models.Levels.lenght == data.lenght,
                                                    
                                                    models.Levels.difficulty >= -3 if data.difficulty == "-" 
                                                    else models.Levels.difficulty == difficulty,
                                                    
                                                    models.Levels.rate == 2 if data.epic == "1" 
                                                    else models.Levels.rate >= 0,
                                                    models.Levels.rate == 1 if data.featured == "1" 
                                                    else models.Levels.rate >= 0,

                                                    models.Levels.id <= 76 if data.gauntlet == "1" 
                                                    else models.Levels.id >= 0
                                                    )
                                                    )
            count = len((await db.execute(result)).scalars().all())

            if data.type == "2":
                database = (await db.execute(result.order_by(models.Levels.likes.desc(), models.Levels.downloads.desc()).offset(page).limit(10))).scalars().all()
            elif data.type == "0":
                answer = (await db.execute(result.filter(models.Levels.name.like(f"%{data.str}%")).order_by(models.Levels.likes.desc(), models.Levels.downloads.desc()).offset(page).limit(10))).scalars().all()
                if answer != []:
                    database = answer
                else:
                    database = (await db.execute(result.filter(models.Levels.id == data.str))).scalars().all()
                
            elif data.type == "5":
                database =(await db.execute(result.filter(models.Levels.authorID == data.str))).scalars().all()
            elif data.type == "6":
                database =(await db.execute(result.filter(models.Levels.rate == 1))).scalars().all()
            elif data.type == "4":
                database =(await db.execute(result.order_by(models.Levels.id.desc()).limit(10).offset(page))).scalars().all()
            elif data.type == "11":
                database =(await db.execute(result.filter(models.Levels.stars > 0).limit(10).offset(page))).scalars().all()
            elif data.type == "16":
                database =(await db.execute(result.filter(models.Levels.rate >= 1))).scalars().all()
            else:
                
                database =(await db.execute(result)).scalars().all()
            if database != []:
                info(f"Level search for '{data.str}'")
                return {'database': database, 'count': count}
            else:
                warning(f"Level Not Found '{data.str}'")
        except Exception as ex:
            error(ex)
            

    @staticmethod
    async def get_level_buid( levelID,db: AsyncSession):
        return (await db.execute(select(models.Levels).filter(models.Levels.id == levelID))).scalars().first()
    
    @staticmethod
    async def get_level_count(db: AsyncSession):
        return (await db.execute(select(models.Levels))).scalar()
        
    # @staticmethod
    # async def downloads_level(levelID,db: AsyncSession):
    #     ret
    
    @staticmethod
    async def delete_level(levelID, db: AsyncSession ):
        db_level = (await db.execute(select(models.Levels).filter(models.Levels.id == levelID))).scalars().first()
        await db.delete(db_level)
        await db.commit()


