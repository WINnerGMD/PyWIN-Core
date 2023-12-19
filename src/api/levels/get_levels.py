from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from logger import info
from src.services.levels import LevelService
from src.utils.crypt import base64_decode
from src.errors import GenericError
router = APIRouter(prefix="/levels", tags=["Levels"])


@router.get("/{lvlid}", summary="Get level by id", responses={
    404: {
        "model": GenericError,
        "description": "level with this ID not found"
    }
}
            )
async def get_levels(lvlid: int) -> JSONResponse:
    info("Request to api | /levels")
    levelData = (await LevelService.get_level_buid(levelID=lvlid, db=db))["database"]
    return {
        "status": "ok",
        "id": levelData.id,
        "LevelName": levelData.name,
        "levelDesc": base64_decode(levelData.desc),
        "stats": {
            "stars": levelData.stars,
            "likes": levelData.likes,
            "downloads": levelData.downloads,
            "coins": levelData.coins,
            "difficulty": levelData.difficulty,
            "rate": levelData.rate,
        },
        "author": {"authorID": levelData.authorID, "authorName": levelData.authorName},
    }
