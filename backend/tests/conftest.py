from app.config import settings
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app

# Use a separate in-memory DB just for tests

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Override the get_db dependency in FastAPI
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Apply override
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Create tables before tests
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after tests (optional)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_client():
    """Provides a test client with isolated DB"""
    return TestClient(app)

@pytest.fixture(scope="function")
def db_session():
    """Provides a fresh DB session for unit tests"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
