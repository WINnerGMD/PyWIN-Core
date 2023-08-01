
from sqlalchemy.orm import Session
from sqlalchemy import Update
from sql import models
from helpers.security import bcrypt_hash
from objects.schemas import UpdateStats
import json

class UserService:




    def register_user(self,db: Session, userName: str, password: str, mail:str):
            if db.query(models.User).filter(models.User.userName == userName).first() != None:
                    return {"code": "-2", "message": "error [UserName already registered]"}
            elif db.query(models.User).filter(models.User.mail == mail).first() != None:
                    return {"code": "-3", "message": "error [User email already registered]"}
            else:  
                passhash = bcrypt_hash(password)
                db_user = models.User(userName=userName, passhash=passhash, mail=mail)
                db.add(db_user)
                db.commit()
                db.refresh(db_user)
                return {"code":"1", "message": "success"}
    

    def get_user_byid(self, db: Session,id: int):
                users = db.query(models.User).filter(models.User.id == id).first()
                # return json.loads(users)
                return users
    
    def update_user(self, db: Session,data: UpdateStats):
            smtp = (
                    Update(models.User).where(data.id== models.User.id).values(data.dict(exclude_unset=True))
            )
            result = db.execute(smtp)
            db.commit()

            return result
    
    def login_user(self, userName: str, password: str, db = Session):
            user = db.query(models.User).filter(models.User.userName == userName).first()
            passhash = bcrypt_hash(password)
            if user == None:
                    return {"code": "-11", "message": "error [User not found]"}
            else:
                    if user.passhash == passhash:
                            return {"code":"1", "message": "success", "id": user.id}
                    else:
                            return {"code":"-11", "message": "error [user's login credentials are incorrect]"}
                


            

