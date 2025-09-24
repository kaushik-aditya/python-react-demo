from app.crud import RecipeRepository
from app import models


def test_repository_get_and_search(db_session):
    # Insert recipe
    r = models.Recipe(
        id=9999,
        name="UnitTest Soup",
        cuisine="TestKitchen",
        cook_time_minutes=15,
        tags="test,unit",
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
