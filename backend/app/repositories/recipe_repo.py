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
        sort_by: str = "id",
        sort_order: str = "asc",
        limit: int = 20,
        offset: int = 0,
    ) -> List[models.Recipe]:
        q = self.db.query(models.Recipe)

        # Eager load children
        q = q.options(
            joinedload(models.Recipe.ingredients),
            joinedload(models.Recipe.instructions),
            joinedload(models.Recipe.tags),
            joinedload(models.Recipe.meal_types),
        )

        if query:
            like = f"%{query}%"
            q = q.outerjoin(models.Tag).outerjoin(models.Ingredient)
            q = q.filter(
                or_(
                    models.Recipe.name.ilike(like),
                    models.Recipe.cuisine.ilike(like),
                    models.Tag.name.ilike(like),
                    models.Ingredient.text.ilike(like),
                )
            )
        if cuisine:
            q = q.filter(models.Recipe.cuisine.ilike(f"%{cuisine}%"))
        if difficulty:
            q = q.filter(models.Recipe.difficulty.ilike(f"%{difficulty}%"))

        # Sorting
        sort_column = getattr(models.Recipe, sort_by, models.Recipe.id)
        q = q.order_by(desc(sort_column) if sort_order == "desc" else asc(sort_column))

        # 🔑 Important in SQLite: prevent duplicates
        q = q.distinct()
        print("custom print:", str(q.statement.compile(compile_kwargs={"literal_binds": True})))

        results = q.offset(offset).limit(limit).all()
        logger.debug("Repo: search returned %d results", len(results))
        return results

