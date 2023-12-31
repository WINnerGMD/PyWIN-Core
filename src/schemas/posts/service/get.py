from pydantic import BaseModel
from src.models import PostsModel


class PostsByUserID(BaseModel):
    database: list[PostsModel]
    count: int
