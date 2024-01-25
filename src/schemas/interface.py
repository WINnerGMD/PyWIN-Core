from pydantic import BaseModel


class InterfaceBaseSchema(BaseModel):
    GDIndex: int
    Name: str
