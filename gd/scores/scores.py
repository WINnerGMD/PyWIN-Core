from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from config import path
from database import get_db
from sqlalchemy.orm import Session
from services.leader_boards import LeaderBoardsService
import json

router = APIRouter()

@router.post(f"{path}/getGJScores20.php", response_class=PlainTextResponse)
async def getScores(db:Session = Depends(get_db)):
    result= await LeaderBoardsService().leaderboard(db=db)
    count = 1
    string = ""
    for i in result:

        iconkit = i.iconkits

 
        string += f"1:{i.userName}:2:{i.id}:3:{i.stars}:4:{i.demons}:6:{count}:7:{i.id}:8:{i.cp}:9:{iconkit['accIcon']}:10:{iconkit['color1']}:11:{iconkit['color2']}:13:{i.coins}:14:0:15:{i.id}:16:{i.id}:17:{i.usr_coins}:46:{i.diamonds}|"
        count += 1
    return string[:-1]

    