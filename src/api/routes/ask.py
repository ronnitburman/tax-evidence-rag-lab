"""POST /ask — Ask a tax-evidence question.

Delegates to core.ask::run_ask_core() — same logic as CLI.
Full RAG pipeline (retrieve → rerank → validate) is pending.
"""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from core.ask import run_ask_core

router = APIRouter(prefix="/ask", tags=["ask"])


class AskRequest(BaseModel):
    """Request body for the /ask endpoint."""

    question: str = Field(
        ...,
        min_length=1,
        description="The tax/legal question to answer.",
        examples=["What is input tax credit eligibility?"],
    )
    model: str | None = Field(
        default=None,
        description="Optional model override.",
    )
    top_k: int | None = Field(
        default=None,
        ge=1,
        le=50,
        description="Number of evidence chunks to retrieve.",
    )


class AskResponse(BaseModel):
    """Response body for the /ask endpoint."""

    question: str
    answer: str
    provider: str
    model: str
    error: str | None = None
    citations: list[str] = []


@router.post("", response_model=AskResponse)
async def ask(body: AskRequest) -> AskResponse:
    """Ask a tax-evidence question using RAG.

    Delegates to core.ask::run_ask_core() — same logic as CLI.
    """
    result = run_ask_core(body.question)

    return AskResponse(
        question=result.question,
        answer=result.answer,
        provider=result.provider,
        model=result.model,
        error=result.error,
        citations=[],
    )
