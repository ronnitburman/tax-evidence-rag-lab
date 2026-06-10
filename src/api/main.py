"""API module — FastAPI application for tax-evidence RAG.

Usage:
    uvicorn api.main:app --reload --port 8000
    uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

Phase 0: Returns a health-check and a placeholder /ask endpoint.
The full RAG pipeline will be wired into /ask in later phases.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.middleware.cors import CORS_SETTINGS
from api.routes.ask import router as ask_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns a FastAPI app with CORS middleware and routes wired.
    """
    app = FastAPI(
        title="TaxEvidence RAG Lab",
        description="Evidence-backed RAG API for tax/legal research — Phase 0 scaffold.",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # ── CORS middleware ────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_SETTINGS["allow_origins"],
        allow_credentials=CORS_SETTINGS["allow_credentials"],
        allow_methods=CORS_SETTINGS["allow_methods"],
        allow_headers=CORS_SETTINGS["allow_headers"],
    )

    # ── Routes ──────────────────────────────────────────────────
    app.include_router(ask_router)

    # ── Health check ────────────────────────────────────────────
    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok", "phase": "0 — scaffold"}

    return app


# Module-level app instance for uvicorn discovery
app = create_app()
