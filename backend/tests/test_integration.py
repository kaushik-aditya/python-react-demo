def test_search_endpoint_returns_200(test_client, db_session):
    # Seed a recipe
    db_session.execute(
        "INSERT INTO recipes (id, name, cuisine, cook_time_minutes, tags) VALUES (1, 'Chicken Curry', 'Indian', 30, 'chicken,curry')"
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
