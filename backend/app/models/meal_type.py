from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class MealType(Base):
    __tablename__ = "meal_types"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"))
    name = Column(String, nullable=False, index=True)

    recipe = relationship("Recipe", back_populates="meal_types")
