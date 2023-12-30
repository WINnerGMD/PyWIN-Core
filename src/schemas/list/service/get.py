from pydantic import BaseModel


class GetList(BaseModel):
    string: str
    page: int
    type: int
    accountID: int
    diff: int
    star: int