from fastapi import APIRouter, Form
from config import path


router = APIRouter()


@router.post(f'{path}/uploadGJLevel21.php')
def upload_level(levelString: str = Form()):
    print(levelString)
    return 1
