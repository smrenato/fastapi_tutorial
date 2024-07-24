from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_tutorial.schemas import UserPublic


# follow AAA architechture
def test_must_return_ok(client: TestClient):
    response = client.get('/')  # Act
    # arrange
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'hello': 'world'}  # Assert


def test_create_user(client: TestClient):
    response = client.post(
        '/users/',
        json={
            'username': 'testname',
            'password': 'passwordteste',
            'email': 'email_test@email.com',
        },
    )

    assert response.status_code == HTTPStatus.CREATED


def test_read_users(client: TestClient):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [],
    }


def test_read_users_with_user(client: TestClient, user):
    response = client.get('/users/')
    user_schema = UserPublic.model_validate(user).model_dump()

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            user_schema,
        ],
    }


def test_get_token(client, user, session):
    response = client.post(
        '/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'acess_token' in token
