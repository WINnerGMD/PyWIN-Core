
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Update,select
from sql import models
from helpers.security import bcrypt_hash
from objects.schemas import UpdateStats


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
    

    async def get_user_byid(self, db: AsyncSession,id: int):
                users = (await db.execute(select(models.Users).filter(models.Users.id == id))).scalars().first()
                # return json.loads(users)
                return users
    
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
                            return {"code":"1", "message": "success", "id": user.id}
                    else:
                            return {"code":"-11", "message": "error [user's login credentials are incorrect]"}
                


            

