from fastapi import FastAPI, Request, Response
from .database.core import Database

import os
from http import HTTPStatus

from contextlib import asynccontextmanager
from .routers import metrics, items
from logging import Logger
from loguru import logger
import traceback


def app_factory(database: Database, logger: Logger = logger) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # On startup:
        await database.open()
        # Let app run:
        yield
        # On shutdown:
        await database.close()

    app = FastAPI(
        lifespan=lifespan,
    )
    app.include_router(metrics)
    app.include_router(items)

    # Attaches a reference of the database object for this app to all
    # requests - can be used to produce per-request sessions
    @app.middleware("http")
    async def db_middleware(request: Request, call_next):
        response = Response(
            "Internal server error",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
        try:
            request.state.db = database.async_sessionmaker()
            response = await call_next(request)
        except Exception as exc:
            logger.error(
                f"Encountered exception when handling request: {str(exc)}",
                exception=str(exc),
                trace_back=traceback.format_exc(),
            )
            await request.state.db.rollback()
        finally:
            await request.state.db.close()
        return response

    return app


app = app_factory(
    Database(
        db_username=os.getenv("DB_USERNAME"),
        db_password=os.getenv("DB_PASSWORD"),
        db_host=os.getenv("DB_HOST"),
        db_name=os.getenv("DB_NAME"),
    ),
)
