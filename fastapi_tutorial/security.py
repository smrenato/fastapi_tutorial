from datetime import datetime, timedelta

from jwt import encode
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo

pwd_context = PasswordHash.recommended()

# TODO: move this SECRET_KEY to a dotenv file
SECRET_KEY = 'secret_key'
ALGORITHM = 'HS256'
ACESS_TOKEN_EXPIRES_MINUTES = 30


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_acess_token(data_claims: dict[str, str]) -> str:
    to_encode = data_claims.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACESS_TOKEN_EXPIRES_MINUTES,
    )

    to_encode.update({'exp': expire})  # pyright: ignore
    encoded_jwt = encode(
        payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt
