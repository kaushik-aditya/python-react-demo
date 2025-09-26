from app import models
from app.repositories.recipe_repo import RecipeRepository

def test_repository_get_and_search(db_session):
    # Insert recipe with related tags
    r = models.Recipe(
        id=9999,
        name="UnitTest Soup",
        cuisine="TestKitchen",
        cook_time_minutes=15,
        tags=[models.Tag(name="test"), models.Tag(name="unit")],   # ✅ LIST of Tag objects
    )
    db_session.add(r)
    db_session.commit()

    repo = RecipeRepository(db_session)

    # Test get by ID
    got = repo.get(9999)
    assert got is not None
    assert got.name == "UnitTest Soup"

    # Test search
    results = repo.search("UnitTest")
    assert any(x.id == 9999 for x in results)
