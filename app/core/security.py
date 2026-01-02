from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt

pwd_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16
)

def hash_password(password: str) -> str:
    return pwd_hasher.hash(password)

def verify_password(password: str, stored: str) -> bool:
    try:
        return pwd_hasher.verify(stored, password)
    except VerifyMismatchError:
        return False

# Decode jwt header without verification
def decode_jwt_header(token: str) -> dict:
    try:
        headers = jwt.get_unverified_header(token)
        return headers
    except jwt.PyJWTError:
        return {}