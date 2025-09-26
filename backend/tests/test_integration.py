import logging
from sqlalchemy import text

logger = logging.getLogger("recipes")


def test_search_endpoint_returns_200(test_client, db_session):
    # Insert recipe core
    db_session.execute(
        text("""
        INSERT INTO recipes (
            id, name, cuisine, cook_time_minutes, difficulty, servings,
            prep_time_minutes, rating, review_count
        ) VALUES (
            1, 'Chicken Curry', 'Indian', 30,
            'Easy', 4, 10, 4.5, 100
        )
        """)
    )

    # Insert tags
    db_session.execute(
        text("INSERT INTO tags (recipe_id, name) VALUES (1, 'chicken'), (1, 'curry')")
    )

    # Insert ingredients
    db_session.execute(
        text("INSERT INTO ingredients (recipe_id, text) VALUES (1, 'chicken'), (1, 'spices')")
    )

    # Insert instructions
    db_session.execute(
        text("INSERT INTO instructions (recipe_id, step_number, text) VALUES (1, 1, 'cook'), (1, 2, 'eat')")
    )

    # Insert meal types
    db_session.execute(
        text("INSERT INTO meal_types (recipe_id, name) VALUES (1, 'lunch')")
    )

    db_session.commit()
    rows = db_session.execute(text("SELECT * FROM recipes")).fetchall()
    print("Recipes in DB:", rows)
    # Test search
    resp = test_client.get("/recipes?difficulty=Easy")
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
