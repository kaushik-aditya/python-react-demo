import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from app import models

logger = logging.getLogger("recipes")


class IngredientRepository:
    """Data access layer for ingredients."""

    def __init__(self, db: Session):
        self.db = db

    def add(self, recipe_id: int, text: str) -> models.Ingredient:
        ingredient = models.Ingredient(recipe_id=recipe_id, text=text)
        self.db.add(ingredient)
        self.db.commit()
        self.db.refresh(ingredient)
        logger.debug("Repo: added ingredient=%s to recipe_id=%s", text, recipe_id)
        return ingredient

    def get_all_for_recipe(self, recipe_id: int) -> List[models.Ingredient]:
        return (
            self.db.query(models.Ingredient)
            .filter(models.Ingredient.recipe_id == recipe_id)
            .all()
        )

    def delete_all_for_recipe(self, recipe_id: int):
        count = (
            self.db.query(models.Ingredient)
            .filter(models.Ingredient.recipe_id == recipe_id)
            .delete()
        )
        self.db.commit()
        logger.debug("Repo: deleted %s ingredients for recipe_id=%s", count, recipe_id)
