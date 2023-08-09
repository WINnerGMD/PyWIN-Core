from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from objects.schemas import UploadComments,UploadPost, GetPost
from sql import models
from services.user import UserService
import datetime
class CommentsService:


    async def upload_comments(self,db:AsyncSession, data: UploadComments):
        db_comment = models.Comments(authorId = data.accountID, content=data.comment, progress = data.percent, levelID= data.levelID, authorName = (await UserService().get_user_byid(db=db, id=data.accountID)).userName)
        db.add(db_comment)
        await db.commit()
        await db.refresh(db_comment)

        return db_comment
    
    async def get_comments(self,level_id,db:AsyncSession):
        return (await db.execute(select(models.Comments).filter(models.Comments.levelID== level_id))).scalars().all()
    

class PostCommentsService:

    @staticmethod
    async def upload_post(db:AsyncSession, data:UploadPost):
        db_post = models.Posts(accountID = data.accountID,content=data.content, timestamp = data.timestamp)

        db.add(db_post)
        await db.commit()
        await db.refresh(db_post)
        return db_post

    @staticmethod
    async def delete_post(postID, db:AsyncSession):
        db_level = (await db.execute(select(models.Posts).filter(models.Posts.id == postID))).scalars().first()
        await db.delete(db_level)
        await db.commit()
    @staticmethod
    async def get_post(db: AsyncSession , data: GetPost):
        return (await db.execute(select(models.Posts).filter(models.Posts.accountID == data.accountID).order_by(models.Posts.id.desc()))).scalars().all()
