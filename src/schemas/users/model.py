from pydantic import BaseModel


class IconkitSchema(BaseModel):
    color1: int
    color2: int
    color3: int
    accIcon: int
    accShip: int
    accJetpack: int
    accBall: int
    accBird: int
    accDart: int
    accGlow: int
    accRobot: int
    accSpider: int
    accSwingCopter: int
    accExplosion: int


class StatsSchema(BaseModel):
    stars: int
    moons: int
    gold_coins: int
    silver_coins: int
    demons: int
    creator_points: int


class APIUserSchema(BaseModel):
    id: int
    username: str
    mail: str
    role: str
    verified: bool
