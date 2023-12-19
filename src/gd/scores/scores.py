from fastapi import APIRouter, Depends, Form
from fastapi.responses import PlainTextResponse
from config import system
from sqlalchemy.orm import Session
from src.services.leader_boards import LeaderBoardsService
from src.helpers.scores import LeaderBoards
from src.objects.userObject import UserGroup

router = APIRouter()


@router.post(
    f"{system.path}/getGJScores20.php", response_class=PlainTextResponse, tags=["Misc"]
)
async def getScores(type: str = Form()):
    score = LeaderBoards(type)
    service = await LeaderBoardsService().leaderboard(db=db, scores_type=score)

    data = await UserGroup(service).GDGetUserGroup()
    return data
