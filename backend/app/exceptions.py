import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status
from app.logger import logger


class AppError(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, error_code: str = "APP_ERROR"):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        trace_id = str(uuid.uuid4())
        logger.warning(
            "AppError at %s [trace_id=%s]: %s",
            request.url, trace_id, exc.message
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.error_code,
                "message": exc.message,
                "status": exc.status_code,
                "path": str(request.url),
                "trace_id": trace_id,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception):
        trace_id = str(uuid.uuid4())
        logger.exception(
            "Unhandled error at %s [trace_id=%s]", request.url, trace_id
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": "INTERNAL_ERROR",
                "message": "Internal Server Error",
                "status": 500,
                "path": str(request.url),
                "trace_id": trace_id,
            },
        )
