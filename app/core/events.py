from typing import Callable
from fastapi import FastAPI
import aioodbc
from app.core.config import DATABASE_NAME, DATABASE_PASSWORD, DATABASE_USERNAME, DATABASE_URL, MIN_CONNECTIONS_COUNT, MAX_CONNECTIONS_COUNT, POSTGRES_SERVER

CONNECTION_STRING = ("DRIVER={PostgreSQL Unicode};"
        f"DATABASE={DATABASE_NAME};"
        f"UID={DATABASE_USERNAME};"
        f"PWD={DATABASE_PASSWORD};"
        f"SERVER={POSTGRES_SERVER};"
        "PORT=5432;")


def startup_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        app.state.pool = await aioodbc.create_pool(
            dsn=CONNECTION_STRING,
            minsize=MIN_CONNECTIONS_COUNT,
            maxsize=MAX_CONNECTIONS_COUNT,
            APP=DATABASE_NAME,
            autocommit=False
        )
    return start_app


def shutdown_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        if app.state.pool is not None:
            await app.state.pool.close()
    return stop_app
