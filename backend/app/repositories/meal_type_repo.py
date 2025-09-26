import logging
from typing import List
from sqlalchemy.orm import Session
from app import models

logger = logging.getLogger("recipes")


class MealTypeRepository:
    """Data access layer for meal types."""

    def __init__(self, db: Session):
        self.db = db

    def add(self, recipe_id: int, name: str) -> models.MealType:
        meal_type = models.MealType(recipe_id=recipe_id, name=name)
        self.db.add(meal_type)
        self.db.commit()
        self.db.refresh(meal_type)
        logger.debug("Repo: added meal_type=%s to recipe_id=%s", name, recipe_id)
        return meal_type

    def get_all_for_recipe(self, recipe_id: int) -> List[models.MealType]:
        return (
            self.db.query(models.MealType)
            .filter(models.MealType.recipe_id == recipe_id)
            .all()
        )

    def delete_all_for_recipe(self, recipe_id: int):
        count = (
            self.db.query(models.MealType)
            .filter(models.MealType.recipe_id == recipe_id)
            .delete()
        )
        self.db.commit()
        logger.debug("Repo: deleted %s meal_types for recipe_id=%s", count, recipe_id)
