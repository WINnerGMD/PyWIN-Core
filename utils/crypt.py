import bcrypt
import base64
import itertools
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import UsersModel
from hashlib import sha1


def base64_encode(string: str) -> str:
    return base64.urlsafe_b64encode(string.encode()).decode()


def base64_decode(string: str) -> str:
    return base64.urlsafe_b64decode(string.encode()).decode()


def bcrypt_hash(password) -> str:
    return bcrypt.hashpw(password, "$2a$12$cFyTWLxu2w5O5mUFVai.be")


def xor_cipher(string: str, key: str) -> str:
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(string, itertools.cycle(key)))


def encode_gjp(password: str) -> str:
    # put it through the xor cipher with the key "37526")
    encoded = xor_cipher(password, "37526")
    # encode the password to base64
    encoded_base64 = base64.b64encode(encoded.encode()).decode()
    encoded_base64 = encoded_base64.replace("+", "-")
    encoded_base64 = encoded_base64.replace("/", "_")
    return encoded_base64


def decode_gjp(gjp: str) -> str:
    # decode the password from base64
    decoded_base64 = base64.b64decode(gjp.encode()).decode()
    # put it through the xor cipher with the key "37526")
    decoded = xor_cipher(decoded_base64, "37526")

    return decoded


async def checkValidGJP(id, gjp, db: AsyncSession) -> bool:
    try:
        password = decode_gjp(gjp)
        bcrypt = bcrypt_hash(password)
        if (
            await db.execute(
                select(UsersModel.passhash).filter(UsersModel.id == id)
            )
        ).scalars().first() == bcrypt:
            return True
        else:
            return False
    except:
        return False


async def sha1_hash(data, salt) -> str:
    hashdata = sha1((data + salt).encode("utf-8"))
    hashed_string = hashdata.hexdigest()
    return hashed_string


def return_hash(string) -> str:
    hash_object = sha1(bytes(string, "utf-8"))
    return hash_object.hexdigest()


def return_hash2(level) -> str:
    data = ""
    l = len(level) // 40
    for i in range(40):
        data += level[i * l]
    return sha1(bytes(data + "xI25fpAapCQg", "utf-8")).hexdigest()


"TODO: make normal crypt file"
