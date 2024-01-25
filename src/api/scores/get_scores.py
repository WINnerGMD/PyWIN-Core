from fastapi import APIRouter
from src.schemas.scores.get import Leaderboard
router = APIRouter(prefix="/scores", tags=["Scores"])


@router.get("/")
async def get_scores() -> Leaderboard:
    return await LeaderBoardsService.leaderboard("top")