import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import httpx

from app import models
from app.models import Recipe
from app.repositories.recipe_repo import RecipeRepository
from app.config import settings

logger = logging.getLogger("recipes")


class RecipeService:
    """Business logic for Recipes with serialization."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = RecipeRepository(db)

    async def load_recipes_from_api(self) -> int:
        """Fetch recipes from external API and insert/update into DB."""
        url = settings.DUMMY_RECIPES_URL
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(url)
        resp.raise_for_status()
        recipes = resp.json().get("recipes", [])

        count = 0
        for data in recipes:
            recipe = Recipe(
                id=data["id"],
                name=data["name"],
                cuisine=data.get("cuisine"),
                difficulty=data.get("difficulty"),
                servings=data.get("servings"),
                prep_time_minutes=data.get("prepTimeMinutes"),
                cook_time_minutes=data.get("cookTimeMinutes"),
                calories_per_serving=data.get("caloriesPerServing"),
                image=data.get("image"),
                rating=data.get("rating"),
                review_count=data.get("reviewCount"),
                user_id=data.get("userId"),
                ingredients=[models.Ingredient(text=i) for i in data.get("ingredients", [])],
                instructions=[
                    models.Instruction(step_number=idx + 1, text=instr)
                    for idx, instr in enumerate(data.get("instructions", []))
                ],
                tags=[models.Tag(name=t) for t in data.get("tags", [])],
                meal_types=[models.MealType(name=m) for m in data.get("mealType", [])],
            )
            if hasattr(self.repo, "upsert"):
                self.repo.upsert(recipe)
            else:
                # fallback: merge via session
                self.db.merge(recipe)
            count += 1

        logger.info("Loaded %s recipes into DB from %s", count, url)
        return count

    def _serialize_recipe(self, recipe: Recipe) -> Dict[str, Any]:
        """Convert SQLAlchemy Recipe object into simplified dict."""
        return {
            "id": recipe.id,
            "name": recipe.name,
            "cuisine": recipe.cuisine,
            "difficulty": recipe.difficulty,
            "servings": recipe.servings,
            "prep_time_minutes": recipe.prep_time_minutes,
            "cook_time_minutes": recipe.cook_time_minutes,
            "calories_per_serving": recipe.calories_per_serving,
            "image": recipe.image,
            "rating": recipe.rating,
            "review_count": recipe.review_count,
            "user_id": recipe.user_id,
            # Arrays of strings
            "ingredients": [i.text for i in recipe.ingredients],
            "tags": [t.name for t in recipe.tags],
            "meal_types": [m.name for m in recipe.meal_types],
            # Instructions → object with step_number as key
            "instructions": {
                instr.text
                for instr in sorted(recipe.instructions, key=lambda x: x.step_number)
            },
        }

    def get_by_id(self, recipe_id: int) -> Optional[Dict[str, Any]]:
        recipe = self.repo.get(recipe_id)
        if recipe:
            logger.info("Service: found recipe id=%s", recipe_id)
            return self._serialize_recipe(recipe)
        else:
            logger.warning("Service: recipe id=%s not found", recipe_id)
            return None

    def search(
        self,
        query: Optional[str] = None,
        cuisine: Optional[str] = None,
        difficulty: Optional[str] = None,
        sort_by: str = "id",
        sort_order: str = "asc",
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
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
        recipes = self.repo.search(
            query=query,
            cuisine=cuisine,
            difficulty=difficulty,
            sort_by=sort_by,
            sort_order=sort_order,
            limit=limit,
            offset=offset,
        )
        return [self._serialize_recipe(r) for r in recipes]
