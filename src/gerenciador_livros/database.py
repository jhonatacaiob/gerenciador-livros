from sqlmodel import Session, create_engine

from .settings import Settings

engine = create_engine(Settings().DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session
