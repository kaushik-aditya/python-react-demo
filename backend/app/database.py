from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# SQLite needs this flag when used with multiple threads (FastAPI runs async workers)
connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}

# Engine = DB connection manager (lazy, opens on first use)
engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)

# Session factory = creates new DB sessions for each request/test
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base = parent class for all ORM models (collects metadata)
Base = declarative_base()


def init_db():
    """
    Initialize database schema depending on environment.
    - dev/test → auto-create tables for quick setup
    - prod → skip auto-creation (expect migrations)
    """
    # Import all models so Base.metadata is aware of them
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
    """
    FastAPI dependency that provides a DB session.
    Ensures proper open/close around each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
