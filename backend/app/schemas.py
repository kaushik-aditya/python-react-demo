from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional


# --- Base schema (shared) ---
class RecipeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    cuisine: str = Field("", max_length=100)
    difficulty: str = Field("", max_length=50)

    servings: int = Field(default=1, ge=1)  # must be >= 1
    prep_time_minutes: int = Field(default=0, ge=0)
    cook_time_minutes: int = Field(default=0, ge=0)
    calories_per_serving: Optional[int] = Field(default=None, ge=0)

    ingredients: List[str] = []
    instructions: List[str] = []
    tags: List[str] = []
    meal_type: List[str] = []


# --- Response schema ---
class RecipeResponse(RecipeBase):
    id: int
    user_id: Optional[int] = None
    image: Optional[HttpUrl] = None
    rating: float = Field(default=0.0, ge=0, le=5)
    review_count: int = Field(default=0, ge=0)

    class Config:
        orm_mode = True


# --- Create schema (for inserts) ---
class RecipeCreate(RecipeBase):
    pass


# --- Update schema (partial updates allowed) ---
class RecipeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    cuisine: Optional[str] = Field(None, max_length=100)
    difficulty: Optional[str] = Field(None, max_length=50)

    servings: Optional[int] = Field(None, ge=1)
    prep_time_minutes: Optional[int] = Field(None, ge=0)
    cook_time_minutes: Optional[int] = Field(None, ge=0)
    calories_per_serving: Optional[int] = Field(None, ge=0)

    ingredients: Optional[List[str]] = None
    instructions: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    meal_type: Optional[List[str]] = None
