from fastapi import APIRouter, Form, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession

from config import path
from database import get_db
from logger import info
from objects.levelObject import LevelObject
from services.levels import LevelService

router = APIRouter()


@router.post(f'{path}/likeGJItem211.php', response_class=PlainTextResponse)
async def like_item(itemID: str = Form(), type: str = Form(), accountID: str = Form(),
                    db: AsyncSession = Depends(get_db)):
    liketype = int(type)
    if liketype == 1:
        service = await LevelService.get_level_buid(levelID=itemID, db=db)
        await LevelObject(service=service, db=db).like(accountID=accountID)
        info('Like')
# class testClass:
#    __slots__ =
