from fastapi import APIRouter,Form,Depends
from config import path
from fastapi.responses import PlainTextResponse
from services.comments import PostCommentsService
from objects.schemas import UploadPost, GetPost
from sqlalchemy.orm import Session
from database import get_db
from services.user import UserService
router = APIRouter()

@router.post(f"{path}/uploadGJAccComment20.php",)
def Upload_post(db: Session = Depends(get_db),
                accountID: str = Form(),
                comment: str = Form(),
                gjp : str = Form()):
    print(gjp)
    post_object = UploadPost(accountID=accountID,content=comment)
    PostCommentsService().upload_post(db = db, data = post_object)
    return ""


@router.post(f"{path}/getGJAccountComments20.php", response_class=PlainTextResponse)
def get_posts(accountID: str = Form(),
              db: Session = Depends(get_db),):
    post_obj= GetPost(accountID=accountID)
    post_string =""
    for i in PostCommentsService().get_post(db=db, data=post_obj):
        post_string += f"2~{i.content}~4~0~9~kafif~6~1756926|"
    return post_string + "#67:0:10"