from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import RecipeResponse
from app.crud import RecipeRepository

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[RecipeResponse])
def search_recipes(
    search: str = Query(..., min_length=1, description="Free text on name/cuisine"),
    db: Session = Depends(get_db),
):
    repo = RecipeRepository(db)
    return repo.search(search)

@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    repo = RecipeRepository(db)
    recipe = repo.get(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe
