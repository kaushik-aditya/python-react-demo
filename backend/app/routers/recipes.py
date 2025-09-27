import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.recipe import PaginatedRecipes, RecipeResponse
from app.services.recipe_service import RecipeService
from app.exceptions import AppError

logger = logging.getLogger("recipes")

router = APIRouter(prefix="/recipes", tags=["Recipes"])


# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[RecipeResponse])
def search_recipes(
    search: Optional[str] = Query(None, min_length=1, description="Free text search (name, cuisine, tags)"),
    cuisine: Optional[str] = Query(None, description="Filter by cuisine"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    sort_by: Optional[str] = Query(None, description="Sort field"),
    sort_order: Optional[str] = Query(None, regex="^(asc|desc)$", description="Sort order: asc or desc"),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Max results"),
    offset: Optional[int] = Query(None, ge=0, description="Pagination offset"),
    db: Session = Depends(get_db),
):
    """
    Search recipes by free-text, filters, sorting, and pagination.
    """
    service = RecipeService(db)
    results = service.search(
        query=search,
        cuisine=cuisine,
        difficulty=difficulty,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        offset=offset,
    )
    
    return results or []


@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """
    Get a recipe by ID.
    """
    service = RecipeService(db)
    recipe = service.get_by_id(recipe_id)
    if not recipe:
        raise AppError("Recipe not found", status.HTTP_404_NOT_FOUND, "NOT_FOUND")
    return recipe
