"""POST /ask — Ask a tax-evidence question.

Phase 0: Returns a placeholder response with the received question.
Will delegate to core.ask::run_ask() once the RAG pipeline is wired.
"""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

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
    citations: list[str] = []
    phase: str = "0 — scaffold"


@router.post("", response_model=AskResponse)
async def ask(body: AskRequest) -> AskResponse:
    """Ask a tax-evidence question using RAG.

    Phase 0: Returns a placeholder. The full RAG pipeline
    (retrieve → rerank → generate → validate) is pending.
    """
    return AskResponse(
        question=body.question,
        answer=(
            "[Phase 0 placeholder] The RAG pipeline is not yet implemented. "
            f"Received question: '{body.question}'. "
            "Subsequent phases will add retrieval, reranking, generation, and citation validation."
        ),
        citations=[],
    )
