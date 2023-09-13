from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from objects.schemas import UploadComments,UploadPost, GetPost
from sql import models
from services.user import UserService
from services.perms import PermissionService
from utils.crypt import base64_decode
class CommentsService:

    @staticmethod
    async def get_comments(level_id,db:AsyncSession):
        return (await db.execute(select(models.Comments).filter(models.Comments.levelID== level_id).order_by(models.Comments.id.desc()))).scalars().all()


    @classmethod
    async def upload_comments(cls,db:AsyncSession, data: UploadComments) -> dict:
        try:
            content = base64_decode(data.comment)
            if content.startswith('/'):
                await cls.commands_handler(data=content[1:], accountID= data.accountID, levelID=data.levelID, db=db)
                return {
                    'status': 'ok',
                    'type': 'command'
                }
            else:
                db_comment = models.Comments(authorId = data.accountID, content=data.comment, progress = data.percent, levelID= data.levelID, authorName = (await UserService().get_user_byid(db=db, id=data.accountID)).userName)
                db.add(db_comment)
                await db.commit()
                await db.refresh(db_comment)

                return {
                    'status': 'ok',
                    'type': 'comment',
                    'data':db_comment
                    }
        except:
            return {
                'status': 'error'
            }
    
    @staticmethod
    async def commands_handler(data: str, accountID: int, levelID: int, db: AsyncSession) -> bool:
        command = data.split(' ')
        name = command[0]
        if name == 'rate':
            stars = command[1]
            difficulty = command[2]
            if difficulty == 'none':
                smtp = {'difficulty': 0, 'stars': stars}
            elif difficulty == 'easy':
                smtp = {'difficulty': 1, 'stars': stars}
            elif difficulty == 'normal':
                smtp = {'difficulty': 2, 'stars': stars}
            elif difficulty == 'hard':
                smtp = {'difficulty': 3, 'stars': stars}
            elif difficulty == 'harder':
                smtp = {'difficulty': 4, 'stars': stars}
            elif difficulty == 'insane':
                smtp = {'difficulty': 5, 'stars': stars}
            elif difficulty == 'easydemon':
                smtp = {'difficulty': 7, 'stars': stars}
            elif difficulty == 'mediumdemon':
                smtp = {'difficulty': 8, 'stars': stars}
            elif difficulty == 'harddemon':
                smtp = {'difficulty': 6, 'stars': stars}
            elif difficulty == 'insanedemon':
                smtp = {'difficulty': 9, 'stars': stars}
            elif difficulty == 'extreme':
                smtp = {'difficulty': 10, 'stars': stars}

        elif name == 'unrate':
            smtp = {'difficulty': 0, 'stars': 0, 'rate': 0}

        elif name == 'nonrate':
            smtp = {'rate': 0}
        elif name == 'featured':
            smtp = {'rate': 1}
        elif name == 'epic':
            smtp = {'rate': 2}
        elif name == 'legendary':
            smtp = {'rate': 3}
        elif name == 'godlike':
            smtp = {'rate': 4}
        (await db.execute(update(models.Levels).where(models.Levels.id == levelID).values(smtp)))
        await db.commit()

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
    async def get_post(db: AsyncSession , usrid:int, page:int):
        offset = int(page) *10 
        count = len((await db.execute(select(models.Posts).filter(models.Posts.accountID == usrid))).scalars().all())
        return {'database': (await db.execute(select(models.Posts).filter(models.Posts.accountID == usrid).limit(10).offset(offset).order_by(models.Posts.id.desc()))).scalars().all(),
                'count': count}
