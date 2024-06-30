import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from src.gerenciador_livros.app import app
from src.gerenciador_livros.database import get_session
from tests.factories import AutorFactory


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def autor(session):
    autor = AutorFactory()
    session.add(autor)
    session.commit()
    session.refresh(autor)

    return autor
