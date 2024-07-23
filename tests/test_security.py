from jwt import decode

from fastapi_tutorial.security import ALGORITHM, SECRET_KEY, create_acess_token


def test_acess_token():
    payload = {'sub': 'test@email.com'}

    token = create_acess_token(data_claims=payload)
    result = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert result['sub'] == payload['sub']
    assert result['exp']
