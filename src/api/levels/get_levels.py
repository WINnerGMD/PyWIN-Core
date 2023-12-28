import numpy
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.errors import GenericError
from src.schemas.levels.model import APILevelSchema
from src.schemas.levels.service.get import GetLevel
from src.services.levels import LevelService, LevelModel
from src.schemas.levels.errors import LevelNotFoundError
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
    levelData: LevelModel = (await LevelService.get_level_buid(levelID=lvlid))["database"]
    return levelData.to_API_model()


@router.post("/search", summary="Searching levels by filter", responses={
    404: {
        "model": GenericError,
        "description": "level with this ID not found"
    }
}
            )
async def get_levelsByFilters(filters: GetLevel) -> list[APILevelSchema]:
    """
      Endpoint to get levels by filters

      Return list of APILevel
    """
    try:
        levelData: list[LevelModel] = (await LevelService.test_get_levels(filters))['database']
        result = list[APILevelSchema]

        for i in numpy.arange(levelData): # Fast range
            result.append(i.to_API_model())

        return result

    except LevelNotFoundError:
        return GenericError("Level Not Found", 404)

    except TypeError as e:
        return GenericError(f"Internal Generic Error {e}", 500)
