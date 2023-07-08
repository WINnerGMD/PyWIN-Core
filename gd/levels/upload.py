from fastapi import APIRouter, Form
from config import path
from database import db

router = APIRouter()


@router.post(f'{path}/uploadGJLevel21.php')
def upload_level(levelString: str = Form(),
                  accountID: str = Form(),
                    levelName: str = Form(),
                    #  levelDesc: str = Form(),
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
    if int(objects) > 100:
        db(f"INSERT INTO `levels`(`name`,`version`, `authorID`, `gameVersion`, `audioTrack`, `levelLength`, `coins`, `original`, `twoPlayer`, `songID`, `requestedStars`, `isLDM`, `objects`, `password`, `uploadDate`, `updateDate`, `string`) VALUES ('{levelName}','{levelVersion}','{accountID}','{gameVersion}','{audioTrack}','{levelLength}','{coins}','{original}','{twoPlayer}','{songID}','{requestedStars}','{ldm}','{objects}','{password}','111','111','{levelString}')")
    return db(f"SELECT * FROM `levels` WHERE `name` = '{levelName}' and `authorID` = '{accountID}'")[0]["id"]
