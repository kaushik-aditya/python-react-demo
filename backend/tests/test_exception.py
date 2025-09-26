import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette import status

from app.exceptions import AppError, add_global_exception_middleware, register_exception_handlers


@pytest.fixture(scope="session")
def app_with_exceptions():
    """Minimal FastAPI app with global exception handlers registered"""
    app = FastAPI()
    register_exception_handlers(app)
    add_global_exception_middleware(app)

    @app.get("/raise-app-error")
    def raise_app_error():
        raise AppError("Custom error occurred", status.HTTP_400_BAD_REQUEST, "CUSTOM_ERR")

    @app.get("/raise-unhandled")
    def raise_unhandled():
        raise ValueError("Boom!")  # should be caught by global Exception handler

    return app


@pytest.fixture(scope="session")
def test_client(app_with_exceptions):
    return TestClient(app_with_exceptions)


def test_app_error_handler_returns_custom_json(test_client):
    resp = test_client.get("/raise-app-error")
    body = resp.json()

    assert resp.status_code == 400
    assert body["error"] == "CUSTOM_ERR"
    assert body["message"] == "Custom error occurred"
    assert body["status"] == 400
    assert "trace_id" in body
    assert body["path"].endswith("/raise-app-error")


def test_unhandled_error_handler_returns_internal_error(test_client):
    resp = test_client.get("/raise-unhandled")
    body = resp.json()

    assert resp.status_code == 500
    assert body["error"] == "INTERNAL_ERROR"
    assert body["message"] == "Internal Server Error"
    assert body["status"] == 500
    assert "trace_id" in body
    assert body["path"].endswith("/raise-unhandled")
