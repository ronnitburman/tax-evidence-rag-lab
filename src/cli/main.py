"""CLI entry point — Typer app exposed as the tax-rag console script.

Usage:
    tax-rag ask "What is input tax credit eligibility?"
    tax-rag ask "question" --model deepseek-chat --top-k 10
    tax-rag version
"""

from __future__ import annotations

from typing import Annotated, Optional

import typer
from rich.console import Console

from core.ask import run_ask

console = Console()

app = typer.Typer(
    name="tax-rag",
    help="Ask questions against tax-evidence documents using RAG.",
    no_args_is_help=True,
)


@app.command()
def ask(
    question: Annotated[
        str,
        typer.Argument(help="The tax/legal question to answer."),
    ],
    model: Annotated[
        Optional[str],
        typer.Option("--model", "-m", help="Override the configured LLM model."),
    ] = None,
    top_k: Annotated[
        Optional[int],
        typer.Option("--top-k", "-k", help="Number of evidence chunks to retrieve."),
    ] = None,
) -> None:
    """Ask a tax-evidence question using RAG."""
    run_ask(question, model=model, top_k=top_k)


@app.command()
def version() -> None:
    """Print version information."""
    console.print("[bold]TaxEvidence RAG Lab[/bold] v0.1.0")
    console.print("Phase 0 — Project Scaffold")
    console.print()
    console.print("Stack: LangChain + DeepSeek + LangGraph + ChromaDB")
    console.print("Status: Scaffold active, pipeline pending (Phases 1–13)")
