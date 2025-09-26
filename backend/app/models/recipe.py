from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)

    # Core fields
    cuisine = Column(String, index=True, default="")
    difficulty = Column(String, default="")
    servings = Column(Integer, default=0)
    prep_time_minutes = Column(Integer, default=0)
    cook_time_minutes = Column(Integer, default=0)
    calories_per_serving = Column(Integer, default=0)

    # Metadata
    user_id = Column(Integer, index=True)
    image = Column(String, default="")
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)

    # Relationships
    ingredients = relationship("Ingredient", back_populates="recipe", cascade="all, delete-orphan")
    instructions = relationship("Instruction", back_populates="recipe", cascade="all, delete-orphan")
    tags = relationship("Tag", back_populates="recipe", cascade="all, delete-orphan")
    meal_types = relationship("MealType", back_populates="recipe", cascade="all, delete-orphan")
