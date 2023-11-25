import hashlib

from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse
from config import system
import itertools
import base64


from utils.crypt import xor_cipher, base64_encode, sha1_hash, base64_decode

router = APIRouter()


@router.post(f"{system.path}/getGJRewards.php", response_class=PlainTextResponse)
async def chest(
    chk: str = Form(),
    accountID: str = Form(),
    gjp: str = Form(),
    device_id: str = Form(..., alias="udid"),
):
    resultchk = xor_cipher(base64_decode(chk[5:]), "59182")
    lam = f"sukaj:{accountID}:{resultchk}:{device_id}:{accountID}:230:1152,36,2,1:4:200:37,71,2,1:2:2"
    encrypt = base64_encode(xor_cipher(lam, "59182"))
    result = (
        "hUiNy"
        + encrypt
        + "|"
        + hashlib.sha1((encrypt + "pC26fpYaQCtg").encode()).hexdigest()
    )
    print(result)
    return result


@router.post(f"{system.path}/getGJChallenges.php", response_class=PlainTextResponse)
async def chest(
    chk: str = Form(),
    accountID: str = Form(),
    gjp: str = Form(),
    device_id: str = Form(..., alias="udid"),
):
    resultchk = xor_cipher(base64_decode(chk[5:]), "19847")
    lam = f"dQbAT:{accountID}:{resultchk}:{device_id}:{accountID}:8203:1,2,2,5,Coin Finder:1,3,10,10,Star Collector:1,1,1000,15,Orb Master"
    encrypt = base64_encode(xor_cipher(lam, "19847"))
    result = (
        "hUiNy"
        + encrypt
        + "|"
        + hashlib.sha1((encrypt + "oC36fpYaPtdg").encode()).hexdigest()
    )
    print(result)
    return result
