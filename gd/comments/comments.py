from fastapi import APIRouter,Form,Depends
from config import path
from fastapi.responses import PlainTextResponse
from services.comments import CommentsService
from objects.schemas import UploadComments
from sqlalchemy.orm import Session
from database import get_db
from services.user import UserService
router = APIRouter()




@router.post(f'{path}/uploadGJComment21.php', response_class=PlainTextResponse)
def upload_comment(
    accountID: str = Form(default=None),
    userName: str = Form(default=None),
    comment: str = Form(default=None),
    levelID: str = Form(default=None),
    percent: str = Form(default=None),
    db: Session = Depends(get_db)
):
    comment_object = UploadComments(userName=userName,accountID=accountID, comment=comment,levelID=levelID,percent=percent)
    answer = CommentsService().upload_comments(db=db, data=comment_object)
    return str(answer.id)
    # return "2~ODk4IHRvIGp1c3QgYmVhdCBpbiBwcmFjdGlzZSBtb2RlIGdnIQ==~3~133533914~4~9~7~2~10~1~9~2 minutes~6~31468976:1~depolo~9~41~10~25~11~10~14~~15~1~16~13735168#5705:0:10"



@router.post(f'{path}/getGJComments21.php', response_class=PlainTextResponse)
def get_user(
    db: Session = Depends(get_db),
    levelID: str = Form(),
    page: str = Form()):

    comments_object = CommentsService().get_comments(db=db , level_id=levelID)
    print(comments_object)
    comment_string = ""
    for i in comments_object:
        userObject = UserService().get_user_byid(db=db, id=i.authorId)
        iconkits = userObject.iconkits
        comment_string +=f"2~{i.content}~3~{i.authorId}~4~9~7~2~10~0~9~fif~6~{i.id}:1~{i.authorName}~9~{iconkits['accIcon']}~12~10~11~11~14~~15~1~16~13735168|"
    return comment_string + "#5705:0:10"
    # return str(comments_object)



