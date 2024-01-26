from pydantic import BaseModel
from ... schemas.users.model import APIUserSchema


class Place(BaseModel):
    place: int
    user: APIUserSchema

    class Config:
        arbitrary_types_allowed = True


class Leaderboard(BaseModel):
    count: int
    leaders: list[Place]

