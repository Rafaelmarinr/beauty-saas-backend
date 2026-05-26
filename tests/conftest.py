from sqlmodel import SQLModel, Session, create_engine
from fastapi.testclient import TestClient
from main import app

import pytest

from db.database import get_session

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# ---------------- OVERRIDE SESSION ----------------

def override_get_session():

    with Session(engine) as session:
        yield session


# ---------------- SESSION FIXTURE ----------------

@pytest.fixture
def session():

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


# ---------------- CLIENT FIXTURE ----------------

@pytest.fixture
def client(session):

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()