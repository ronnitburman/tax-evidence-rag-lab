"""Core business logic for the ask flow — no CLI or HTTP dependency."""

from __future__ import annotations

from typing import Optional

from rich.console import Console
from rich.panel import Panel

from config.settings import Settings, load_settings

console = Console()


def run_ask(
    question: str,
    *,
    model: Optional[str] = None,
    top_k: Optional[int] = None,
    settings: Optional[Settings] = None,
) -> None:
    """Execute the core ask flow.

    Pure business logic — called by CLI, API, or tests.
    No Typer, no FastAPI, no HTTP dependency.

    Args:
        question: The tax/legal question to answer.
        model: Optional model override.
        top_k: Optional top-k override.
        settings: Optional pre-loaded settings (useful for testing).
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

    # ── Status ────────────────────────────────────────────────
    console.print()
    console.print(
        "[yellow]⚠[/yellow]  The LangGraph RAG pipeline is not yet implemented. "
        "This is the Phase 0 scaffold.\n"
        "    Subsequent phases will add: ingestion → chunking → embeddings → "
        "retrieval → reranking → generation → citation validation."
    )
    console.print()
