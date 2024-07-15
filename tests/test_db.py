from sqlalchemy import select

from fastapi_tutorial.models import User


def test_create_user(session):
    user = User(
        username='cabecinha',
        password='12345',
        email='email@email.com',
    )
    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'email@email.com')
    )
    assert result.email == 'email@email.com'
