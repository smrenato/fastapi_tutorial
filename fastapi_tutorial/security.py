from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from fastapi_tutorial.database import get_session
from fastapi_tutorial.models import User

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

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


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if not username:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    user = session.scalar(select(User).where(User.username == username))

    if not user:
        raise credentials_exception

    return user
