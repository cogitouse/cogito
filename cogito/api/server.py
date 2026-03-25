"""FastAPI server for Cogito."""

from __future__ import annotations

import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cogito.config.settings import CogitoSettings
from cogito.api.routes import build_router

logger = logging.getLogger(__name__)


def create_app(settings: CogitoSettings) -> FastAPI:
    app = FastAPI(
        title="Cogito API",
        description="AI consciousness and AGI readiness evaluation",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.api.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(build_router(settings))
    return app


def start_server(
    settings: CogitoSettings,
    host: str = "0.0.0.0",
    port: int = 8420,
) -> None:
    app = create_app(settings)
    logger.info("starting Cogito API on %s:%d", host, port)
    uvicorn.run(app, host=host, port=port)
