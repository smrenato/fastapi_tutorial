from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_tutorial.app import app


# follow AAA architechture
def test_must_return_ok():
    ...
    client = TestClient(app)  # Arrange

    response = client.get('/')  # Act
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'hello': 'world'}  # Assert
