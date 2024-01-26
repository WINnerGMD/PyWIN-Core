from pydantic import BaseModel
from .... models import PostsModel


class PostsByUserID(BaseModel):
    database: list[PostsModel]
    count: int
