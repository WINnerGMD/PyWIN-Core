from fastapi import APIRouter,Form, Depends
from fastapi.responses import PlainTextResponse
from config import path
from services.likes import LikesService
from objects.schemas import likeItem
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

router = APIRouter()


@router.post(f'{path}/likeGJItem211.php', response_class=PlainTextResponse)
async def likeItem211(itemID: str = Form(), type: str = Form(), accountID:str =  Form(), like: str = Form(), db: AsyncSession = Depends(get_db)):
   like = likeItem(itemID=itemID,type=type,like=like,accountID=accountID)
   return (await LikesService().upload_like(db=db, data=like))


# class testClass:
#    __slots__ = 