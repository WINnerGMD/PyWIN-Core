from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    JSON,
)

from .. database import Base


class UsersModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    userName = Column(String(255), unique=True)
    mail = Column(String(255), unique=True)
    role = Column(Integer, default=0)
    passhash = Column(String(255))
    verified = Column(Boolean, default=False)
    stars = Column(Integer, default=0)
    diamonds = Column(Integer, default=0)
    coins = Column(Integer, default=0)
    usr_coins = Column(Integer, default=0)
    demons = Column(Integer, default=0)
    cp = Column(Integer, default=0)
    iconkits = Column(
        JSON,
        default={
            "color1": 0,
            "color2": 3,
            "accBall": 1,
            "accBird": 1,
            "accDart": 1,
            "accGlow": 0,
            "accIcon": 1,
            "accShip": 1,
            "accRobot": 1,
            "accSpider": 1,
            "accExplosion": 1,
        },
    )
    networks = Column(JSON)
    ip = Column(String(255))

    def __repr__(self):
        shprot = {
            "id": self.id,
            "userName": self.userName,
            "mail": self.mail,
            "role": self.role,
            "passhash": self.passhash,
            "verified": self.verified,
            "stats": {
                "stars": self.stars,
                "diamonds": self.diamonds,
                "coins": self.coins,
                "usr_coins": self.usr_coins,
                "demons": self.demons,
                "cp": self.cp,
            },
        }

        return str(shprot)
