from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_tutorial.database import get_session
from fastapi_tutorial.models import User
from fastapi_tutorial.schemas import (
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI()


@app.get('/')
def hello_world():
    return {'hello': 'world'}


@app.get('/users/', response_model=UserList)
def read_users(session: Session = Depends(get_session), limit: int = 10):
    users = session.scalars(select(User))
    return {'users': users}


@app.post('/users/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if db_user is not None:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='email already exists',
            )
    db_user = User(
        username=user.username, email=user.email, password=user.password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
