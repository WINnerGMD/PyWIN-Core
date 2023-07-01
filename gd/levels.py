import hashlib
from fastapi import APIRouter, Request, Form
from fastapi.responses import PlainTextResponse,  HTMLResponse
from database import db

router = APIRouter(
    prefix="",
    tags=["levels"]
)

def sha1(string):
    sha1 = hashlib.sha1()
    sha1.update(string.encode('utf-8'))
    hashed_string = sha1.hexdigest()
    return hashed_string

def levelHash(data):
    hash = ""
    for x in range(len(data)):
        hash = hash+str(data[x]["levelID"])[0]+str(data[x]["levelID"])[len(str(data[x]["levelID"]))-1]+str(data[x]["stars"])+str(data[x]["coins"])
    return sha1(hash+"xI25fpAapCQg")

@router.post("/winnertests/getGJLevels21.php", response_class=HTMLResponse)
def get_level(page: str = Form()):
    levelsDataHash = []
    levelString = ""
    userString = ""

    result = db("SELECT * FROM levels")
    
    for row in result[int(page+"0"):][:10]:
        levelsDataHash += [{"levelID":row["levelID"],"stars":row["starStars"],"coins":row["coins"]}]

        levelString += f'1:{row["levelID"]}:2:{row["levelName"]}:5:{row["levelVersion"]}:6:{row["userID"]}:8:10:9:{row["starDifficulty"]}0:10:{row["downloads"]}:12:{row["audioTrack"]}:13:{row["gameVersion"]}:14:{row["likes"]}:17:{row["starDemon"]}:43:{row["starDemonDiff"]}:25:{row["starAuto"]}:18:{row["starStars"]}:19:{row["starFeatured"]}:42:{row["starEpic"]}:45:{row["objects"]}:3:{row["levelDesc"]}:15:{row["levelLength"]}:30:{row["original"]}:31:{row["twoPlayer"]}:37:{row["coins"]}:38:{row["starCoins"]}:39:{row["requestedStars"]}:46:1:47:2:35:{row["songID"]}|'

        userString += f'{row["userID"]}:PyWin-Core:{row["accountID"]}|'
   
    return f"{levelString}#{userString}##{len(result)}:{int(page+'0')}:10#{levelHash(levelsDataHash)}"
