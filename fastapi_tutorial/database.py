from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastapi_tutorial.settings import Settings

engine = create_engine(Settings().DATA_BASE_URL)  # type: ignore


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
