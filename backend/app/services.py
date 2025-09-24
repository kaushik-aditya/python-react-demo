import requests
from sqlalchemy.orm import Session
from app import models
from app.config import settings
from app.logger import logger

class RecipeService:
    def __init__(self, db: Session):
        self.db = db

    def to_tags_str(self, tags):
        if isinstance(tags, list):
            return ",".join([str(t) for t in tags])
        return str(tags or "")

def load_recipes_from_api(db: Session):
    resp = requests.get(settings.DUMMY_RECIPES_URL, timeout=30)
    resp.raise_for_status()
    data = resp.json().get("recipes", [])
    count = 0
    for r in data:
        recipe = models.Recipe(
            id=r.get("id"),
            name=r.get("name", ""),
            cuisine=r.get("cuisine", "") or "",
            cook_time_minutes=int(r.get("cookTimeMinutes", 0) or 0),
            tags=",".join(r.get("tags", []) or []),
        )
        db.merge(recipe)  # upsert
        count += 1
    db.commit()
    logger.info("Loaded %s recipes from %s", count, settings.DUMMY_RECIPES_URL)
