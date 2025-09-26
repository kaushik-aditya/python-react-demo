import logging
from sqlalchemy import text

logger = logging.getLogger("recipes")

def test_search_endpoint_returns_200(test_client, db_session):
    db_session.execute(
        text("""
        INSERT INTO recipes (
            id, name, cuisine, cook_time_minutes, tags, difficulty, servings,
            prep_time_minutes, ingredients, instructions, meal_type, rating, review_count
        ) VALUES (
            1, 'Chicken Curry', 'Indian', 30,
            json('["chicken","curry"]'), 'Easy', 4,
            10, json('["chicken","spices"]'), json('["cook","eat"]'),
            json('["lunch"]'), 4.5, 100
        )
        """)
    )
    db_session.commit()

    resp = test_client.get("/recipes?search=chicken")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert any("Chicken Curry" in r["name"] for r in data)


def test_get_by_id_404(test_client):
    resp = test_client.get("/recipes/0")
    assert resp.status_code == 404
    body = resp.json()
    assert body["error"] == "NOT_FOUND"
    assert body["message"] == "Recipe not found"
    assert body["status"] == 404
    assert "trace_id" in body
    assert body["path"].endswith("/recipes/0")

