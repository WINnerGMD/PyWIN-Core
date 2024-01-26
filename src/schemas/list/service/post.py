from pydantic import BaseModel


class UploadList(BaseModel):
    accountID: int
    listName: str
    listDesc: str
    listLevelsID: str
    difficultyIcon: int

