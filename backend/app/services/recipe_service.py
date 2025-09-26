import logging
from typing import List, Optional
from sqlalchemy.orm import Session
import httpx

from app import models
from app.models import Recipe
from app.repositories.recipe_repo import RecipeRepository
from app.config import settings

logger = logging.getLogger("recipes")


class RecipeService:
    """Business logic for Recipes."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = RecipeRepository(db)

    async def load_recipes_from_api(self) -> int:
        """Fetch recipes from external API and insert/update into DB."""
        url = settings.DUMMY_RECIPES_URL
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json().get("recipes", [])

        count = 0
        for r in data:
            recipe = models.Recipe(
                id=r["id"],
                name=r.get("name", ""),
                cuisine=r.get("cuisine", "") or "",
                cook_time_minutes=int(r.get("cookTimeMinutes", 0) or 0),
                tags=",".join(r.get("tags", []) or []),
            )
            if hasattr(self.repo, "upsert"):
                self.repo.upsert(recipe)
            else:
                # fallback: merge via session
                self.db.merge(recipe)
            count += 1

        logger.info("Loaded %s recipes into DB from %s", count, url)
        return count

    def get_by_id(self, recipe_id: int) -> Optional[Recipe]:
        recipe = self.repo.get(recipe_id)
        if recipe:
            logger.info("Service: found recipe id=%s", recipe_id)
        else:
            logger.warning("Service: recipe id=%s not found", recipe_id)
        return recipe

    def search(
        self,
        query: Optional[str] = None,
        cuisine: Optional[str] = None,
        difficulty: Optional[str] = None,
        sort_by: str = "id",
        sort_order: str = "asc",
        limit: int = 20,
        offset: int = 0,
    ) -> List[Recipe]:
        logger.debug(
            "Service: searching recipes query=%s cuisine=%s difficulty=%s sort=%s %s limit=%s offset=%s",
            query,
            cuisine,
            difficulty,
            sort_by,
            sort_order,
            limit,
            offset,
        )
        return self.repo.search(
            query=query,
            cuisine=cuisine,
            difficulty=difficulty,
            sort_by=sort_by,
            sort_order=sort_order,
            limit=limit,
            offset=offset,
        )
