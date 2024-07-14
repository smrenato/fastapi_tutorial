from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry

table_registry = registry()


class Base(DeclarativeBase): ...


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),  # pylint: disable=[not-callable]
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        onupdate=func.now(),  # pylint: disable=[not-callable]
        server_default=func.now(),  # pylint: disable=[not-callable]
    )

    def __repr__(self) -> str:
        return f"""User(id={self.id}, username={self.username},
                email={self.email}, created_at={self.created_at})"""
