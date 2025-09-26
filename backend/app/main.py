from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import recipes
from app.database import init_db, SessionLocal
from app.logger import setup_logging, logger
from app.exceptions import add_global_exception_middleware, register_exception_handlers
from app.services.recipe_service import RecipeService


def create_app() -> FastAPI:
    app = FastAPI(
        title="Recipes API",
        version="1.0.0",
        description="FastAPI + SQLite in-memory Recipes service",
    )

    # Setup logging
    setup_logging()

    # Register global exception handlers
    register_exception_handlers(app)
    add_global_exception_middleware(app)
    # CORS (allow everything for now — good for dev/demo)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )    

    return app


app = create_app()
# Routers
app.include_router(recipes.router, tags=["Recipes"])

# Status/health route
@app.get("/status", tags=["Health"])
def get_status():
    return {
        "status": "ok",
        "app": app.title,
        "version": app.version,
    }

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing database and loading seed data from DummyJSON...")
    init_db()
    db = SessionLocal()
    service = RecipeService(db)
    try:
        await service.load_recipes_from_api()
        logger.info("Seed data loaded successfully.")
    except Exception as e:
        logger.error("Failed to load seed data", exc_info=e)
    finally:
        db.close()

