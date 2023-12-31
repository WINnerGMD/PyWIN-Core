import bcrypt
import base64
import itertools
from sqlalchemy.ext.asyncio import AsyncSession
from src.depends.user import UsersRepository, UsersModel
from hashlib import sha1


# TODO: Make this model faster


def base64_encode(string: str) -> str:
    return base64.urlsafe_b64encode(string.encode()).decode()


def base64_decode(string: str) -> str:
    return base64.urlsafe_b64decode(string.encode()).decode()


def bcrypt_hash(password) -> str:
    return bcrypt.hashpw(password, "$2a$12$cFyTWLxu2w5O5mUFVai.be")


def xor_cipher(string: str, key: str) -> str:
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(string, itertools.cycle(key)))


async def sha1_hash(data, salt) -> str:
    hashdata = sha1((data + salt).encode("utf-8"))
    hashed_string = hashdata.hexdigest()
    return hashed_string


async def checkValidGJP2(id: int, gjp2: str) -> bool:
    """
    Check Geometry Dash Password 2
    """

    try:
        user = await UsersRepository.find_byid(id)
        if user.passhash == gjp2:
            return True
        else:
            return False
    except:
        return False


async def checkValidGJP2byName(name: str, gjp2: str) -> bool:
    """
      Check Geometry Dash Password 2
      """

    try:
        user: UsersModel = await UsersRepository().find_byfield(UsersModel.userName == name)
        if user is not None:
            if user.passhash == gjp2:
                return True
            else:
                return False
        else:
            raise Exception("user not found")
    except:
        return False


def return_hash(string: str, salt: str) -> str:
    hash_object = sha1(bytes(string + salt, "utf-8"))
    return hash_object.hexdigest()


def return_hash2(level) -> str:
    data = ""
    l = len(level) // 40
    for i in range(40):
        data += level[i * l]
    return sha1(bytes(data + "xI25fpAapCQg", "utf-8")).hexdigest()

# TODO: make normal crypt file
