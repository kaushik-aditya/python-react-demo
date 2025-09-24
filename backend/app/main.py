from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers import recipes
from app.database import init_db, SessionLocal
from app.logger import setup_logging, logger
from app.exceptions import register_exception_handlers
from app.services import load_recipes_from_api

app = FastAPI(title="Recipes API", version="1.0.0", description="FastAPI + SQLite in-memory Recipes service")

# Logging & exception handlers
setup_logging()
register_exception_handlers(app)

# CORS for frontend dev server and docker network
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    logger.info("Initializing database and loading seed data from DummyJSON...")
    init_db()
    # Load data once at startup
    db = SessionLocal()
    try:
        load_recipes_from_api(db)
        logger.info("Seed data loaded successfully.")
    finally:
        db.close()

# Routers
app.include_router(recipes.router, prefix="/recipes", tags=["Recipes"])
# Status/health route
@app.get("/status", tags=["Health"])
def get_status():
    return {
        "status": "ok",
        "app": app.title,
        "version": app.version
    }