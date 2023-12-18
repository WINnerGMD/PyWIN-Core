from fastapi import APIRouter, Depends
from database import get_db
from logger import info
from src.services.levels import LevelService
from src.utils.crypt import base64_decode

router = APIRouter(prefix="/api", tags=["API"])


@router.get("/levels/{lvlid}")
async def get_levels(lvlid: int, db=Depends(get_db)):
    info("Request to api | /api/levels")
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
