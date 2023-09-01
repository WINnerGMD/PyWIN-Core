from fastapi import APIRouter, Form, Depends
from config import path
from services.levels import LevelService
from objects.schemas import UploadLevel
from database import get_db
from sqlalchemy.orm import Session
router = APIRouter()


@router.post(f'{path}/uploadGJLevel21.php')
async def upload_level(db: Session = Depends(get_db),
                    levelString: str = Form(),
                  accountID: str = Form(),
                    levelName: str = Form(),
                     levelDesc: str = Form(default='WyBoZXkgaGUgZGlkbid0IHB1dCBhIGRlc2NyaXB0aW9uIF0='),
                      levelVersion: str = Form(), 
                      levelLength: str = Form(),
                        audioTrack: str = Form(),
                        password: str = Form(),
                            original: str = Form(),
                            twoPlayer: str = Form(),
                            songID: str = Form(),
                            objects: str = Form(),
                            coins: str = Form(),
                            requestedStars: str = Form(),
                            ldm: str = Form(),
                            gameVersion: str = Form()
):
    SystemObj = UploadLevel(
                levelString = levelString,
                accountID = accountID,
                levelName = levelName,
                levelDesc = levelDesc,
                levelVersion = levelVersion,
                levelLength = levelLength,
                audioTrack = audioTrack,
                password = password,
                original = original,
                twoPlayer = twoPlayer,
                songID = songID ,
                objects = objects,
                coins = coins,
                requestedStars = requestedStars,
                ldm = ldm,
                gameVersion = gameVersion
                )
    return (await LevelService().upload_level(db=db, data=SystemObj)).id
