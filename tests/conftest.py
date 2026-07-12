import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db
import os


TEST_DATABASE_URL: str = os.getenv("TEST_DATABASE_URL", "postgresql://postgres@localhost:5432/url_test")

engine = create_engine(TEST_DATABASE_URL)
TestingSession = sessionmaker(bind=engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def clean_tables():
    """Wipe all data before every test so tests don't leak state into each other."""
    with engine.begin() as conn:
        conn.execute(Base.metadata.tables["clicks_analytics"].delete())
        conn.execute(Base.metadata.tables["urls"].delete())
        conn.execute(Base.metadata.tables["users"].delete())
    yield


@pytest.fixture
def client():
    return TestClient(app)