from sqlalchemy.orm import Session
from objects.schemas import UploadComments,UploadPost, GetPost
from sql import models
from services.user import UserService

class CommentsService:


    def upload_comments(self,db:Session, data: UploadComments):
        db_comment = models.Comments(authorId = data.accountID, content=data.comment, progress = data.percent, levelID= data.levelID, authorName = UserService().get_user_byid(db=db, id=data.accountID).userName)
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)

        return db_comment
    
    def get_comments(self,level_id,db:Session):
        return db.query(models.Comments).filter(models.Comments.levelID== level_id).all()
    

class PostCommentsService:

    def upload_post(self,db:Session, data:UploadPost):
        db_post = models.posts(accountID = data.accountID,content=data.content)

        db.add(db_post)
        db.commit()
        db.refresh(db_post)


    def get_post(self, db: Session , data: GetPost):
        return db.query(models.posts).filter(models.posts.accountID == data.accountID).order_by(models.posts.id.desc()).all()
