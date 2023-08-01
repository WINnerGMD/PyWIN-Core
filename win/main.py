from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix='/_pywin', tags=["pywin"])



@router.get('/')
def get_pywin():
    return {"version": '1'}


class User(BaseModel):
    text: str
    version: int


@router.put('/origins')
def update_origins(data: User):
    print(data.version)
    return data.text

@router.get('/origins')
def get_origins():
    return {"version": '1'}
