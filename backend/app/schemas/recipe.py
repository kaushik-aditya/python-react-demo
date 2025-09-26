from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, ConfigDict

from app.schemas.ingredient import IngredientResponse
from app.schemas.instruction import InstructionResponse
from app.schemas.tag import TagResponse
from app.schemas.meal_type import MealTypeResponse


class RecipeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    cuisine: str = Field("", max_length=100)
    difficulty: str = Field("", max_length=50)
    servings: int = Field(default=1, ge=1)
    prep_time_minutes: int = Field(default=0, ge=0)
    cook_time_minutes: int = Field(default=0, ge=0)
    calories_per_serving: Optional[int] = Field(default=None, ge=0)


class RecipeCreate(RecipeBase):
    # When creating → accept child objects too
    ingredients: List[str] = []
    instructions: List[str] = []
    tags: List[str] = []
    meal_types: List[str] = []


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
    meal_types: Optional[List[str]] = None


class RecipeResponse(RecipeBase):
    id: int
    user_id: Optional[int] = None
    image: Optional[HttpUrl] = None
    rating: float = Field(default=0.0, ge=0, le=5)
    review_count: int = Field(default=0, ge=0)

    # Nested children
    ingredients: List[IngredientResponse] = []
    instructions: List[InstructionResponse] = []
    tags: List[TagResponse] = []
    meal_types: List[MealTypeResponse] = []

    model_config = ConfigDict(from_attributes=True)
