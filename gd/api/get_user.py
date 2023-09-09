from fastapi import APIRouter, Depends
from services.user import UserService
from database import get_db
from logger import info
router = APIRouter(prefix='/api', tags=['API'])

@router.get('/users/{usrid}')
async def get_user(usrid:int , db=Depends(get_db)):
    info(f'Request to api | /api/users/{usrid}')
    userData = await UserService.get_user_byid(id=usrid, db=db)
    return {
        'status': 'ok',
        'userName': userData.userName,
        'role': userData.role,
        'stats': {
            'stars': userData.stars,
            'diamonds': userData.diamonds,
            'coins': userData.coins,


        'iconkits': userData.iconkits
        
        }

    }