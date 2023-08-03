from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from config import path
from database import get_db
from sqlalchemy.orm import Session
from services.leader_boards import LeaderBoardsService
import json

router = APIRouter()

@router.post(f"{path}/getGJScores20.php", response_class=PlainTextResponse)
def getScores(db:Session = Depends(get_db)):
    result= LeaderBoardsService().leaderboard(db=db)
    count = 1
    string = ""
    for i in result:

        iconkit = i.iconkits

        string += f"1:{i.userName}:2:{i.id}:13:{i.coins}:17:{i.usr_coins}:6:{count}:9:{iconkit['accIcon']}:10:{iconkit['color1']}:11:{iconkit['color2']}:14:0:15:{iconkit['accGlow']}:16:{i.id}:3:{i.stars}:8:0:46:{i.diamonds}:4:{i.demons}|"
        count += 1
    return string

    