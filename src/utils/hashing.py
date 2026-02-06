import bcrypt
import hashlib
from config import security


def hash_password(password: str) -> str:
    match security.hash_algorithm:
        case "bcrypt":
            return bcrypt.hashpw(
                password.encode(), 
                bcrypt.gensalt(rounds=security.bcrypt_rounds)
            ).decode()
        case "sha1":
            return hashlib.sha1(password.encode()).hexdigest()
        case "sha256":
            return hashlib.sha256(password.encode()).hexdigest()
        case _:
            return bcrypt.hashpw(
                password.encode(), 
                bcrypt.gensalt(rounds=12)
            ).decode()


def verify_password(password: str, hashed: str) -> bool:
    match security.hash_algorithm:
        case "bcrypt":
            return bcrypt.checkpw(password.encode(), hashed.encode())
        case "sha1":
            return hashlib.sha1(password.encode()).hexdigest() == hashed
        case "sha256":
            return hashlib.sha256(password.encode()).hexdigest() == hashed
        case _:
            return bcrypt.checkpw(password.encode(), hashed.encode())
