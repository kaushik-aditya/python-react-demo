from pydantic import BaseModel, ConfigDict
from typing import Optional


class MealTypeBase(BaseModel):
    name: str


class MealTypeCreate(MealTypeBase):
    pass


class MealTypeResponse(MealTypeBase):
    id: int
    recipe_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)
