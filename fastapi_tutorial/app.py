from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from .schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

fakeDB = []


@app.get('/')
def hello_world():
    return {'hello': 'world'}


@app.get('/users/', response_model=UserList)
def read_users():
    return {'users': fakeDB}


@app.post('/users/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema):
    user_whit_id = UserDB(id=len(fakeDB) + 1, **user.model_dump())
    fakeDB.append(user_whit_id)
    return user_whit_id


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(fakeDB):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_whit_id = UserDB(**user.model_dump(), id=user_id)
    fakeDB[user_id - 1] = user_whit_id

    return user_whit_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(fakeDB):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    return {'message': 'user deleted'}
