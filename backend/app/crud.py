from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc
from app import models


class RecipeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, recipe_id: int) -> Optional[models.Recipe]:
        """Fetch a recipe by ID"""
        return (
            self.db.query(models.Recipe)
            .filter(models.Recipe.id == recipe_id)
            .first()
        )

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
        """
        Search recipes with optional filters and sorting.
        - query: free-text search (name, cuisine, tags)
        - cuisine: filter by cuisine
        - difficulty: filter by difficulty
        - sort_by: which column to sort on
        - sort_order: asc/desc
        - limit/offset: pagination
        """
        q = self.db.query(models.Recipe)

        # Free-text search (name, cuisine, tags)
        if query:
            like = f"%{query}%"
            q = q.filter(
                or_(
                    models.Recipe.name.ilike(like),
                    models.Recipe.cuisine.ilike(like),
                    models.Recipe.tags.ilike(like),
                )
            )

        # Filters
        if cuisine:
            q = q.filter(models.Recipe.cuisine.ilike(f"%{cuisine}%"))
        if difficulty:
            q = q.filter(models.Recipe.difficulty.ilike(f"%{difficulty}%"))

        # Sorting
        sort_column = getattr(models.Recipe, sort_by, models.Recipe.id)
        if sort_order == "desc":
            q = q.order_by(desc(sort_column))
        else:
            q = q.order_by(asc(sort_column))

        # Pagination
        return q.offset(offset).limit(limit).all()

    def list_all(self, limit: int = 100, offset: int = 0) -> List[models.Recipe]:
        """Fetch all recipes with pagination (no filters)"""
        return (
            self.db.query(models.Recipe)
            .order_by(models.Recipe.id.asc())
            .offset(offset)
            .limit(limit)
            .all()
        )
