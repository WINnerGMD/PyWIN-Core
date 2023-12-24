from fastapi import APIRouter, Form, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from config import system
from src.models import GauntletsModel
from src.services.levels import LevelService
from src.utils.gdform import gd_dict_str
from src.utils.crypt import return_hash
from src.depends.gauntlets import GauntletsRepository
router = APIRouter(tags=["Packs"], default_response_class=PlainTextResponse)

@router.post(f"{system.path}/getGJGauntlets21.php")
async def gauntlets():
    gauntlets = await GauntletsRepository().find_all()
    response = ""
    hash_string = ""
    for gn in gauntlets:
        single_response = {1: gn.indexpack, 3: gn.levels}

        hash_string += f"{gn.indexpack}{gn.levels}"
        response += gd_dict_str(single_response) + "|"

    response = response[:-1] + f"#{return_hash(hash_string, 'xI25fpAapCQg')}"
    return response

@router.post(f"{system.path}/getGJMapPacks21.php")
async def map_packs(page: str = Form()):
    packs = await LevelService.get_map_packs(db=db, page=int(page))
    packstrings = []
    packhash = ""
    for pack in packs["database"]:
        packstrings.append(
            gd_dict_str(
                {
                    1: pack.id,
                    2: pack.name,
                    3: pack.levels,
                    4: pack.stars,
                    5: pack.coins,
                    6: pack.difficulty,
                    7: pack.text_color,
                    8: pack.bar_color,
                }
            )
        )
        packhash += f"{str(pack.id)[0]}{str(pack.id)[-1]}{pack.stars}{pack.coins}"
    return (
        "|".join(packstrings)
        + f"#{packs['count']}:{int(page) * 10}:10#"
        + return_hash(packhash, 'xI25fpAapCQg')
    )



