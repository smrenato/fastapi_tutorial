from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastapi_tutorial.settings import Settings

engine = create_engine(url=Settings().DATA_BASE_URL)  # pyright: ignore[reportCallIssue]


def get_session() -> Generator[Session]:  # pragma: no cover
    with Session(bind=engine) as session:
        yield session
