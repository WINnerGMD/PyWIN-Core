# from fastapi import APIRouter,Form
# from fastapi.responses import PlainTextResponse
# from config import path
import itertools
import base64


# from utils.crypt import xor_cipher
# router = APIRouter()
def xor_cipher(string: str, key: str) -> str:
    return ("").join(chr(ord(x) ^ ord(y)) for x, y in zip(string, itertools.cycle(key)))


def base64_decode(string: str) -> str:
    return base64.urlsafe_b64decode(string.encode()).decode("ascii")


# @router.post(f'{path}/getGJComments21.php', response_class=PlainTextResponse)
# async def chest(rewardType: str = Form(),
#                 accountID: str = Form(),
#                 gjp: str = Form(),):
#     cheststr = {

#     }
print(
    xor_cipher(
        base64_decode(
            "SaVRPfENHSAEPDQgACAELBwEEBAMBCAIFCQEIAhgIBloAGA1TXgEYCQELARhaBAAFBQkCC1EAAQYCBgwBCwsGDAwLCQMACx0LBBkIHQ4IBAMGCgIFAwILAQIVBgkeABUIAgMPCw=="
        ),
        "59182",
    )
)
