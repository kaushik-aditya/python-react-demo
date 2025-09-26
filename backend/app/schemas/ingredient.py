from pydantic import BaseModel, ConfigDict
from typing import Optional


class IngredientBase(BaseModel):
    text: str


class IngredientCreate(IngredientBase):
    pass


class IngredientResponse(IngredientBase):
    id: int
    recipe_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)
