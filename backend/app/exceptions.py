import logging
import uuid
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("recipes")


class AppError(Exception):
    """Custom application error you can raise in services/routers."""
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, error: str = "APP_ERROR"):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error = error

def add_global_exception_middleware(app: FastAPI):
    @app.middleware("http")
    async def catch_all_exceptions(request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            trace_id = str(uuid.uuid4())
            logger.error(f"Middleware caught unhandled error at {request.url} [trace_id={trace_id}]", exc_info=exc)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "INTERNAL_ERROR",
                    "message": "Internal Server Error",
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "trace_id": trace_id,
                    "path": str(request.url.path),
                },
            )

def register_exception_handlers(app):
    """Register global exception handlers for AppError, HTTP errors, and generic Exception."""

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        trace_id = str(uuid.uuid4())
        logger.warning(f"AppError at {request.url} [trace_id={trace_id}]: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.error,
                "message": exc.message,
                "status": exc.status_code,
                "trace_id": trace_id,
                "path": str(request.url.path),
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        trace_id = str(uuid.uuid4())
        logger.error(f"HTTPException at {request.url} [trace_id={trace_id}]: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "NOT_FOUND" if exc.status_code == 404 else "HTTP_ERROR",
                "message": exc.detail or "HTTP Error",
                "status": exc.status_code,
                "trace_id": trace_id,
                "path": str(request.url.path),
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        trace_id = str(uuid.uuid4())
        logger.error(f"Unhandled error at {request.url} [trace_id={trace_id}]", exc_info=exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "INTERNAL_ERROR",
                "message": "Internal Server Error",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "trace_id": trace_id,
                "path": str(request.url.path),
            },
        )
