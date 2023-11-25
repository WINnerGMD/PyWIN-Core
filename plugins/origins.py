from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from objects.levelObject import LevelObject, LevelGroup
from services.levels import LevelService


# Main plugin parser file
# Не советую что либо тут изменять. Тут также летят запросы на сервер,
# по этому со сломаным модулем, ошибки могут не регаться,
# и вы не сможете расширенно управлять ядром

router = APIRouter()


class PyWIN:
    "fastapi"

    router = router

    def __init__(self, plugin_name):
        self.name = plugin_name
        "TODO: Make verification"

    def __str__(self):
        return self.name

    @staticmethod
    async def get_level(id: int | tuple, db: AsyncSession):
        match type(id):
            case int:
                return LevelObject(
                    await LevelService.get_level_buid(levelID=id, db=db), db=db
                )
