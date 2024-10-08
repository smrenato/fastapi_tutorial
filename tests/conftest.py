import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapi_tutorial.app import app
from fastapi_tutorial.database import get_session
from fastapi_tutorial.models import User, table_registry
from fastapi_tutorial.security import get_password_hash


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registry.metadata.create_all(engine)
    # test
    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    def get_overide_session():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_overide_session
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user(session):
    passwd = '12345'

    user = User(
        username='test',
        password=get_password_hash(password=passwd),
        email='test@email.com',
    )

    # atrribute only for test
    user.clean_password = passwd  # pyright: ignore
    session.add(user)
    session.commit()
    session.refresh(user)

    return user
