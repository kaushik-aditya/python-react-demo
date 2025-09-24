import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = os.getenv("ENV", "dev")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR: str = os.getenv("LOG_DIR", "./logs")
    DUMMY_RECIPES_URL: str = os.getenv(
        "DUMMY_RECIPES_URL", "https://dummyjson.com/recipes"
    )

    @property
    def DATABASE_URL(self) -> str:
        if self.ENV == "dev":
            # In-memory DB for quick dev cycles
            return "sqlite+pysqlite:///:memory:"
        elif self.ENV == "test":
            # File-based DB for reproducible tests
            return "sqlite+pysqlite:///./test.db"
        elif self.ENV == "prod":
            # Persistent DB for production
            return "sqlite+pysqlite:///./recipes.db"
        else:
            raise ValueError(f"Unknown environment: {self.ENV}")


settings = Settings()
