from pydantic import BaseModel, ConfigDict
from typing import Optional


class InstructionBase(BaseModel):
    step_number: int
    text: str


class InstructionCreate(InstructionBase):
    pass


class InstructionResponse(InstructionBase):
    id: int
    recipe_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)
