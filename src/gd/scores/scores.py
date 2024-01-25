from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse
from config import system
from src.services.leader_boards import LeaderBoardsService
from src.helpers.scores import LeaderBoards
from src.objects.userObject import UserGroup

router = APIRouter()


@router.post(
    f"/getGJScores20.php", response_class=PlainTextResponse, tags=["Misc"]
)
async def getScores(type: str = Form()):
    score = LeaderBoards(type)
    service = await LeaderBoardsService.leaderboard(scores_type=score)

    data = await UserGroup(service).GDGetUserGroup()
    return data
