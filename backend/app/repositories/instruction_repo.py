import logging
from typing import List
from sqlalchemy.orm import Session
from app import models

logger = logging.getLogger("recipes")


class InstructionRepository:
    """Data access layer for instructions."""

    def __init__(self, db: Session):
        self.db = db

    def add(self, recipe_id: int, step_number: int, text: str) -> models.Instruction:
        instruction = models.Instruction(recipe_id=recipe_id, step_number=step_number, text=text)
        self.db.add(instruction)
        self.db.commit()
        self.db.refresh(instruction)
        logger.debug("Repo: added instruction step=%s to recipe_id=%s", step_number, recipe_id)
        return instruction

    def get_all_for_recipe(self, recipe_id: int) -> List[models.Instruction]:
        return (
            self.db.query(models.Instruction)
            .filter(models.Instruction.recipe_id == recipe_id)
            .order_by(models.Instruction.step_number)
            .all()
        )

    def delete_all_for_recipe(self, recipe_id: int):
        count = (
            self.db.query(models.Instruction)
            .filter(models.Instruction.recipe_id == recipe_id)
            .delete()
        )
        self.db.commit()
        logger.debug("Repo: deleted %s instructions for recipe_id=%s", count, recipe_id)
