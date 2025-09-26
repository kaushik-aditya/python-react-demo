from pydantic import BaseModel, ConfigDict
from typing import Optional


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagResponse(TagBase):
    id: int
    recipe_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)
