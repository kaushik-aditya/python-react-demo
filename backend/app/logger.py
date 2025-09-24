import logging
import os
from app.config import settings

LOG_DIR = settings.LOG_DIR
logger = logging.getLogger("recipes")

def setup_logging():
    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")

    # Console handler (always used)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    handlers = [console_handler]

    if settings.ENV != "test":
        # Only add file handlers in dev/prod
        os.makedirs(LOG_DIR, exist_ok=True)

        info_handler = logging.FileHandler(os.path.join(LOG_DIR, "api.log"))
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(formatter)

        error_handler = logging.FileHandler(os.path.join(LOG_DIR, "api-error.log"))
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)

        handlers.extend([info_handler, error_handler])

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers = handlers

    # Uvicorn loggers
    for uvicorn_logger in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        log = logging.getLogger(uvicorn_logger)
        log.setLevel(level)
        log.handlers = handlers

    logger.info("Logging initialized at level %s (env=%s)", settings.LOG_LEVEL, settings.ENV)
