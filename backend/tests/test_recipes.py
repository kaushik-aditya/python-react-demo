import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app


# --- Setup in-memory test DB ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# --- Fixtures ---
@pytest.fixture
def mock_api_response():
    return {
        "recipes": [
            {
                "id": 1,
                "name": "Chicken Curry",
                "cuisine": "Indian",
                "cookTimeMinutes": 30,
                "tags": ["spicy", "chicken"],
            },
            {
                "id": 2,
                "name": "Pasta",
                "cuisine": "Italian",
                "cookTimeMinutes": 15,
                "tags": ["vegetarian", "easy"],
            },
        ]
    }


def test_search_recipes():
    resp = client.get("/recipes/?search=Chicken")
    body = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    assert len(body) == 1
    assert body[0]["name"] == "Chicken Curry"


def test_get_recipe_by_id():
    resp = client.get("/recipes/1")
    body = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    assert body["id"] == 1
    assert body["name"] == "Chicken Curry"


def test_get_recipe_not_found():
    resp = client.get("/recipes/9999")
    body = resp.json()

    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert body["error"] == "NOT_FOUND"
    assert body["message"] == "Recipe not found"
