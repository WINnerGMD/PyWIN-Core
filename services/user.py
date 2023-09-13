
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Update,select
from sql import models
from utils.crypt import bcrypt_hash
from objects.schemas import UpdateStats
from services.perms import PermissionService
from logger import info, error

class UserService:




    async def register_user(self,db: AsyncSession, userName: str, password: str, mail:str):
            request = select(models.Users).filter(models.Users.userName == userName)
            if (await db.execute(request)).scalars().first() != None:
                    return {"code": "-2", "message": "error [UserName already registered]"}
            elif (await db.execute(select(models.Users).filter(models.Users.mail == mail))).scalars().first() != None:
                    return {"code": "-3", "message": "error [User email already registered]"}
            else:  
                passhash = bcrypt_hash(password)
                db_user = models.Users(userName=userName, passhash=passhash, mail=mail)
                db.add(db_user)
                await db.commit()
                await db.refresh(db_user)
                return {"code":"1", "message": "success"}
    
    @staticmethod
    async def get_user_byid(db: AsyncSession,id: int):
                try:   
                        user = (await db.execute(select(models.Users).filter(models.Users.id == id))).scalars().first()
                        if user == None:
                               raise Exception("User not found")
        
                        rank  = len((await db.execute(select(models.Users).filter(models.Users.stars >= user.stars))).scalars().all())
                        permissions = await PermissionService.get_permissions(id=user.role, db=db)
                        return {
                               'status': 'ok',
                               'database':user, 
                                'rank': rank,
                                'permissions':permissions}
                
                except Exception as ex:
                       return {
                               'status': 'error',
                               'details':ex
                               }
                
                
    @staticmethod
    async def upload_message(db: AsyncSession,
                             authorID,
                             recipientID,
                             subject,
                             body):
           try:
                message = models.Messages(
                        authorID=authorID,
                        recipientID=recipientID,
                        subject=subject,
                        body=body
                )
                db.add(message)
                await db.commit()
                await db.refresh(message)
                return "1"
           except Exception as ex:
                  error(ex)
                  return "-1"
    async def update_user(self, db: AsyncSession,data: UpdateStats):
            smtp = (
                    Update(models.Users).where(data.id== models.Users.id).values(data.dict(exclude_unset=True))
            )
            result = await db.execute(smtp)
            await db.commit()

            return result
    
    async def login_user(self, userName: str, password: str, db = AsyncSession):
            user = (await db.execute(select(models.Users).filter(models.Users.userName == userName))).scalars().first()
            passhash = bcrypt_hash(password)
            print(user)
            if user == None:
                    return {"code": "-11", "message": "error [User not found]"}
            else:
                    if user.passhash == passhash:
                            if user.verified == True:
                                return {"code":"1", "message": "success", "id": user.id}
                            else:
                                return {'code': '-12', 'message':  "error [the user's account is disabled]"}
                    else:
                            return {"code":"-11", "message": "error [user's login credentials are incorrect]"}
                


            

