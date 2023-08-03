from sqlalchemy.orm import Session
from sql import models

class LeaderBoardsService:
    

    def leaderboard(self, db: Session):
        return db.query(models.User).order_by(models.User.stars.desc()).all()