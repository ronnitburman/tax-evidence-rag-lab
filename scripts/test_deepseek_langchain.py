#!/usr/bin/env python3
"""Test script: verify LangChain DeepSeek integration.

Usage:
    python scripts/test_deepseek_langchain.py

Prerequisites:
    - DEEPSEEK_API_KEY set in .env or exported in shell
    - LLM_PROVIDER=deepseek (default)

What it does:
    1. Loads settings from .env
    2. Creates a ChatDeepSeek via the factory
    3. Sends a minimal test prompt
    4. Prints the model response
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure src/ is importable when running from repo root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from rich.console import Console
from rich.panel import Panel

from config.settings import load_settings
from generation.llm_factory import LLMFactoryError, get_chat_model

console = Console()


def main() -> None:
    console.rule("[bold blue]LangChain DeepSeek — Integration Test[/bold blue]")
    console.print()

    # ── Load settings ─────────────────────────────────────────
    console.print("[bold]1. Loading settings...[/bold]")
    try:
        settings = load_settings()
    except Exception as exc:
        console.print(f"[red]✗ Failed to load settings:[/red] {exc}")
        sys.exit(1)

    console.print(f"   Provider : {settings.llm_provider}")
    console.print(f"   Model    : {settings.deepseek_model}")
    console.print(f"   API Key  : {settings.masked_api_key()}")
    console.print()

    # ── Build model via factory ───────────────────────────────
    console.print("[bold]2. Creating chat model via factory...[/bold]")
    try:
        llm = get_chat_model(settings)
    except LLMFactoryError as exc:
        console.print(f"[red]✗ LLMFactoryError:[/red] {exc}")
        sys.exit(1)
    except Exception as exc:
        console.print(f"[red]✗ Unexpected error:[/red] {exc}")
        sys.exit(1)

    console.print(f"   [green]✓[/green] Model created: {llm.__class__.__name__}")
    console.print()

    # ── Send test prompt ──────────────────────────────────────
    console.print("[bold]3. Sending test prompt...[/bold]")
    test_prompt = 'Return {"ok": true, "provider": "deepseek"} as JSON only.'

    try:
        response = llm.invoke(test_prompt)
    except Exception as exc:
        console.print(f"[red]✗ Invocation failed:[/red] {exc}")
        sys.exit(1)

    console.print()
    console.print(Panel.fit(
        str(response.content),
        title="[bold]Model Response[/bold]",
        border_style="green",
    ))
    console.print()

    # ── Verify response ───────────────────────────────────────
    console.print("[bold]4. Verifying response...[/bold]")
    content = str(response.content).strip()
    if "ok" in content.lower() or "deepseek" in content.lower():
        console.print("   [green]✓[/green] Response contains expected keywords.")
    else:
        console.print("   [yellow]⚠[/yellow] Response format unexpected but model is working.")
    console.print()

    console.rule("[bold green]Test Passed[/bold green]")


if __name__ == "__main__":
    main()
