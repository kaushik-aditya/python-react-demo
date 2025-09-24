from sqlalchemy import Column, Integer, String, Float, Text
from app.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)

    # Core recipe fields
    cuisine = Column(String, index=True, default="")
    difficulty = Column(String, default="")
    servings = Column(Integer, default=0)
    prep_time_minutes = Column(Integer, default=0)
    cook_time_minutes = Column(Integer, default=0)
    calories_per_serving = Column(Integer, default=0)

    # Arrays in JSON → stored as comma-separated text
    ingredients = Column(Text, default="")    # list of ingredients
    instructions = Column(Text, default="")   # list of steps
    tags = Column(Text, default="")           # list of tags
    meal_type = Column(Text, default="")      # list of meal types

    # Metadata
    user_id = Column(Integer, index=True)
    image = Column(String, default="")
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
