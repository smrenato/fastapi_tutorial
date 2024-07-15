from http import HTTPStatus

from fastapi.testclient import TestClient


# follow AAA architechture
def test_must_return_ok(client: TestClient):
    response = client.get('/')  # Act
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'hello': 'world'}  # Assert


def test_create_user(client: TestClient):
    response = client.post(
        '/users/',
        json={
            'username': 'testname',
            'password': '12345',
            'email': 'test@email.com',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'testname',
        'id': 1,
        'email': 'test@email.com',
    }


# deixar para depois, esperar o DB estar implementado
# def test_read_users(client: TestClient):
#     response = client.get('/users/')
#     assert response.status_code == HTTPStatus.OK
#     # assert response.json()


# def test_update_users(client: TestClient):
#     response = client.put(
#         '/users/id',
#         json={'username': 'test_username',
# 'email': 'test@email.com', 'id': 1},
#     )
#     assert response.json() == {
#         'username': 'test_username',
#         'email': 'test@email.com',
#         'id': 1,
#     }
