import logging
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, asc, desc

from app import models

logger = logging.getLogger("recipes")


class RecipeRepository:
    """Data access layer for recipes."""

    def __init__(self, db: Session):
        self.db = db

    def upsert(self, recipe: models.Recipe):
        self.db.merge(recipe)
        self.db.commit()

    def add(self, recipe: models.Recipe) -> models.Recipe:
        self.db.add(recipe)
        self.db.commit()
        self.db.refresh(recipe)
        logger.debug("Repo: added recipe id=%s name=%s", recipe.id, recipe.name)
        return recipe

    def get(self, recipe_id: int) -> Optional[models.Recipe]:
        recipe = (
            self.db.query(models.Recipe)
            .options(
                joinedload(models.Recipe.ingredients),
                joinedload(models.Recipe.instructions),
                joinedload(models.Recipe.tags),
                joinedload(models.Recipe.meal_types),
            )
            .filter(models.Recipe.id == recipe_id)
            .first()
        )
        logger.debug("Repo: fetched recipe by id=%s -> %s", recipe_id, recipe)
        return recipe

    def delete(self, recipe_id: int) -> bool:
        recipe = self.db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
        if not recipe:
            return False
        self.db.delete(recipe)
        self.db.commit()
        logger.debug("Repo: deleted recipe id=%s", recipe_id)
        return True

    def search(
    self,
    query: Optional[str] = None,
    cuisine: Optional[str] = None,
    difficulty: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[models.Recipe]:
        q = self.db.query(models.Recipe)

        if query:
            like = f"%{query}%"
            q = q.outerjoin(models.Tag).outerjoin(models.Ingredient)
            q = q.filter(
                or_(
                    models.Recipe.name.ilike(like),
                    models.Recipe.cuisine.ilike(like),
                )
            )

        if cuisine:
            q = q.filter(models.Recipe.cuisine.ilike(f"%{cuisine}%"))
        if difficulty:
            q = q.filter(models.Recipe.difficulty.ilike(f"%{difficulty}%"))

        # Only apply sorting if explicitly passed
        if sort_by:
            sort_column = getattr(models.Recipe, sort_by, models.Recipe.id)
            if sort_order == "desc":
                q = q.order_by(desc(sort_column))
            else:
                q = q.order_by(asc(sort_column))

        # Only apply pagination if explicitly passed
        if offset is not None:
            q = q.offset(offset)
        if limit is not None:
            q = q.limit(limit)

        q = q.distinct()

        results = q.all()
        logger.debug("Repo: search returned %d results", len(results))
        return results

    
    def count(
        self,
        query: Optional[str] = None,
        cuisine: Optional[str] = None,
        difficulty: Optional[str] = None,
    ) -> int:
        """
        Return the total number of recipes that match the filters (ignores limit/offset).
        """
        q = self.db.query(models.Recipe)

        if query:
            like = f"%{query}%"
            q = q.outerjoin(models.Tag).outerjoin(models.Ingredient).outerjoin(models.MealType)
            q = q.filter(
                or_(
                    models.Recipe.name.ilike(like),
                    models.Recipe.cuisine.ilike(like),
                )
            )

        if cuisine:
            q = q.filter(models.Recipe.cuisine.ilike(f"%{cuisine}%"))
        if difficulty:
            q = q.filter(models.Recipe.difficulty.ilike(f"%{difficulty}%"))

        total = q.distinct().count()
        logger.debug("Repo: count returned %d", total)
        return total

