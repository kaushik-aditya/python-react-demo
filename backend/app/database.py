from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Shared in-memory SQLite setup
connect_args = {"check_same_thread": False}
if "sqlite" in settings.DATABASE_URL and "file::memory:" in settings.DATABASE_URL:
    connect_args["uri"] = True

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    future=True,  # optional but recommended
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

def init_db():
    """Initialize schema (auto-create in dev/test)."""
    from app.models.recipe import Recipe
    from app.models.ingredient import Ingredient
    from app.models.instruction import Instruction
    from app.models.tag import Tag
    from app.models.meal_type import MealType

    if settings.ENV in ["dev", "test"]:
        Base.metadata.create_all(bind=engine)
    elif settings.ENV == "prod":
        from app.logger import logger
        logger.info("Skipping auto-create of tables in prod. Use migrations instead.")

def get_db():
    """FastAPI dependency for DB session lifecycle."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
