from sqlmodel import Session, create_engine

from .settings import Settings

engine = create_engine(Settings().DATABASE_URL)  # type: ignore


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
