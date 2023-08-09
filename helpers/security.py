import bcrypt
import base64
import itertools
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sql import models
from hashlib import sha1
def bcrypt_hash(password):
    return bcrypt.hashpw(password.encode(), b'$2b$12$VWAACqVFSNt8bIiWVXdsyO').decode()

def xor_cipher(string: str, key: str) -> str:
    return ("").join(chr(ord(x) ^ ord(y)) for x, y in zip(string, itertools.cycle(key)))

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

async def chechValid(id,gjp,db: AsyncSession):
      try:
        password = decode_gjp(gjp)
        bcrypt = bcrypt_hash(password)
        if (await db.execute(select(models.Users.passhash).filter(models.Users.id == id))).scalars().first() == bcrypt:
                return True
        else:
                return False
      except:
            return False
      




def sha1_hash(content, solt):
      return sha1(content+solt)