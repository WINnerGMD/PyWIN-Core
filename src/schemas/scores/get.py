from pydantic import BaseModel
from src.schemas.users.model import APIUserSchema
from src.models.user import UsersModel

class Place(BaseModel):
    place: int
    user: UsersModel

    class Config:
        arbitrary_types_allowed = True


class Leaderboard(BaseModel):
    count: int
    leaders: list[Place]

