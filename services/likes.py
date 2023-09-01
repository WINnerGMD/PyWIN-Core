from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from objects.schemas import likeItem,LikeUpload
from sql import models
from sqlalchemy import Update

class LikesService:


    @staticmethod
    async def upload_like(db: AsyncSession, data: likeItem):
        if (await db.execute(select(models.Users.verified).filter(models.Users.id == data.accountID))).scalars().first() == True:
            if int(data.type) == 1:
                if int(data.like) == 1:
                    request = int((await db.execute(select(models.Levels.likes).filter(models.Levels.id == data.itemID))).scalars().first())
                    item = LikeUpload(likes=request+1)
                    smtp = (
                            Update(models.Levels).where(data.itemID == models.Levels.id).values(item.dict(exclude_unset=True))
                        )
                    result = await db.execute(smtp)
                    await db.commit()
                    return "1"
                
                elif int(data.like) == 0:
                    request = int((await db.execute(select(models.Levels.likes).filter(models.Levels.id == data.itemID))).scalars().first())
                    item = LikeUpload(likes=request-1)
                    smtp = (
                            Update(models.Levels).where(data.itemID == models.Levels.id).values(item.dict(exclude_unset=True))
                        )
                    result = db.execute(smtp)
                    await db.commit()
                    return "1"
            elif int(data.type) == 2:
                pass
            elif int(data.type) == 3:

                if int(data.like) == 1:
                    request = int(db.query(models.Posts.likes).filter(models.Posts.id == data.itemID).first()[0])
                    item = LikeUpload(likes=request+1)
                    smtp = (
                            Update(models.Posts).where(data.itemID == models.Posts.id).values(item.dict(exclude_unset=True))
                        )
                    result = db.execute(smtp)
                    await db.commit()
                    return "1"
                
                elif int(data.like) == 0:
                    request = int(db.query(models.Posts.likes).filter(models.Posts.id == data.itemID).first()[0])
                    item = LikeUpload(likes=request-1)
                    smtp = (
                            Update(models.Posts).where(data.itemID == models.Posts.id).values(item.dict(exclude_unset=True))
                        )
                    result = db.execute(smtp)
                    await db.commit()
                    return "1"
        else:
            return {"error": "Unauthorized"}