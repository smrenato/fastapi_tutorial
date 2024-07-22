from http import HTTPStatus

from fastapi.testclient import TestClient


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
