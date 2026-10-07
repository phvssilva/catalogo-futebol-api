import os
from collections.abc import Generator

from sqlalchemy.engine import Engine
from sqlmodel import Session, create_engine


def _create_engine() -> Engine:
    database_url = os.getenv("DATABASE_URL", "sqlite:///./catalogo.db")
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    return create_engine(database_url, connect_args=connect_args)


engine = _create_engine()


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
