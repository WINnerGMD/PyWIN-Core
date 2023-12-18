from pydantic import BaseModel


class GenericError(BaseModel):
    status: str = "error"
    details: str