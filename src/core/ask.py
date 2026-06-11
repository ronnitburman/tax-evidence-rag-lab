"""Core business logic for the ask flow — no CLI or HTTP dependency."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from rich.console import Console
from rich.panel import Panel

from config.settings import Settings, load_settings
from generation.llm_factory import LLMFactoryError, get_chat_model

console = Console()


# ── Data types ──────────────────────────────────────────────────


@dataclass
class AskResult:
    """Structured result of an ask operation.

    Returned by run_ask_core() — consumed by CLI (for Rich display),
    API (for JSON response), and tests (for assertions).
    """

    question: str
    answer: str
    provider: str
    model: str
    error: str | None = None


# ── Core logic (CLI + API + tests) ──────────────────────────────


def run_ask_core(
    question: str,
    *,
    settings: Settings | None = None,
) -> AskResult:
    """Run the ask pipeline and return a structured result.

    Pure business logic. No Typer, no FastAPI, no Rich output.
    Called by CLI, API, and tests.

    Args:
        question: The tax/legal question to answer.
        settings: Optional pre-loaded settings.

    Returns:
        AskResult with answer, provider, model, and optional error.
    """
    if settings is None:
        settings = load_settings()

    provider = settings.llm_provider
    model_name = settings.deepseek_model

    try:
        llm = get_chat_model(settings)
        response = llm.invoke(question)
        return AskResult(
            question=question,
            answer=str(response.content),
            provider=provider,
            model=model_name,
        )
    except LLMFactoryError as exc:
        return AskResult(
            question=question,
            answer=str(exc),
            provider=provider,
            model=model_name,
            error=str(exc),
        )


# ── CLI output (Rich formatting — called by CLI only) ───────────


def run_ask(
    question: str,
    *,
    model: Optional[str] = None,
    top_k: Optional[int] = None,
    settings: Optional[Settings] = None,
) -> None:
    """Execute the ask flow with Rich console output.

    Args:
        question: The tax/legal question to answer.
        model: Optional CLI model override.
        top_k: Optional CLI top-k override.
        settings: Optional pre-loaded settings.
    """
    if settings is None:
        settings = load_settings()

    effective_model = model or settings.deepseek_model
    effective_top_k = top_k or settings.default_top_k

    # ── Header ────────────────────────────────────────────────
    console.rule("[bold blue]TaxEvidence RAG Lab[/bold blue]")
    console.print()

    # ── Question ──────────────────────────────────────────────
    console.print(Panel.fit(
        question,
        title="[bold]Your Question[/bold]",
        border_style="cyan",
    ))

    # ── Configuration ─────────────────────────────────────────
    console.print()
    console.print("[bold]Runtime Configuration[/bold]")
    console.print(f"  • LLM Provider : {settings.llm_provider}")
    console.print(f"  • Model        : {effective_model}")
    console.print(f"  • Temperature  : {settings.deepseek_temperature}")
    console.print(f"  • Max Tokens   : {settings.deepseek_max_tokens}")
    console.print(f"  • Top-K        : {effective_top_k}")
    console.print(f"  • Candidate-K  : {settings.default_candidate_k}")
    console.print(f"  • Chroma Dir   : {settings.chroma_persist_dir}")
    console.print(f"  • API Key      : {settings.masked_api_key()}")

    # ── LLM (Phase 1) — delegate to core function ─────────────
    console.print()
    console.print("[bold]LLM Response[/bold]")

    result = run_ask_core(question, settings=settings)

    if result.error:
        console.print(Panel.fit(
            f"[red]{result.error}[/red]",
            title="[bold red]LLM Error[/bold red]",
            border_style="red",
        ))
    else:
        console.print(Panel.fit(
            result.answer,
            title=f"[bold]{result.provider} / {result.model}[/bold]",
            border_style="green",
        ))

    # ── Status ────────────────────────────────────────────────
    console.print()
    console.print(
        "[yellow]⚠[/yellow]  RAG pipeline (Phases 2–12) is not yet implemented. "
        "Currently running: Phase 0 (scaffold) + Phase 1 (LLM client).\n"
        "    Upcoming: ingestion → chunking → embeddings → "
        "retrieval → reranking → generation → citation validation."
    )
    console.print()
