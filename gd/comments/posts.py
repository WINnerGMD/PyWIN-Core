from fastapi import APIRouter,Form,Depends,HTTPException
from config import path
from fastapi.responses import PlainTextResponse
from services.comments import PostCommentsService
from objects.schemas import UploadPost, GetPost
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from services.user import UserService
from utils.crypt import checkValidGJP
from datetime import datetime
router = APIRouter()

@router.post(f"{path}/uploadGJAccComment20.php",)
async def Upload_post(db: AsyncSession = Depends(get_db),
                accountID: str = Form(),
                comment: str = Form(),
                gjp : str = Form()):
    timestamp = datetime.utcnow()
    if await checkValidGJP(id=accountID,gjp=gjp,db=db) == True:
        post_object = UploadPost(accountID=accountID,content=comment,timestamp=timestamp)
        await PostCommentsService().upload_post(db = db, data = post_object)
        return "1"
    else:
        raise HTTPException(401,"удачи!!!")


@router.post(f"{path}/deleteGJAccComment20.php", response_class=PlainTextResponse)
async def get_posts(accountID: str = Form(),
                    gjp: str = Form(),
                    commentID: str = Form(),
                    db: AsyncSession = Depends(get_db)):
    if await checkValidGJP(id=accountID, gjp=gjp, db=db):
        await PostCommentsService.delete_post(postID=commentID, db=db)

    return "1"