from pydantic import BaseModel


class UserSchema(BaseModel):
    id = int
    userName = str
    mail = str
    role = str
    passhash = str
    verified = bool


class UserStatsSchema(BaseModel):
    stars = int
    diamonds = int
    coins = int
    usr_coins = int
    demons = int
    cp = int
