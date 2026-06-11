"""LLM factory — returns the configured chat model based on LLM_PROVIDER.

Supported providers:
    deepseek → ChatDeepSeek (langchain-deepseek)
    mock     → MockChatModel (fake for tests/offline dev)

Design principle: the evidence pipeline (retrieval, reranking, citation validation,
LangGraph) never imports a specific vendor class directly. It calls get_chat_model().
"""

from __future__ import annotations

import os

from langchain_core.language_models import BaseChatModel

from config.settings import Settings, load_settings
from generation.mock_llm import MockChatModel


class LLMFactoryError(Exception):
    """Raised when the LLM cannot be created (missing key, unknown provider, etc.)."""


def get_chat_model(settings: Settings | None = None) -> BaseChatModel:
    """Return a LangChain BaseChatModel for the configured provider.

    Args:
        settings: Optional pre-loaded settings. If None, load_settings() is called.

    Returns:
        A BaseChatModel instance (ChatDeepSeek or MockChatModel).

    Raises:
        LLMFactoryError: If API key is missing for a live provider, or provider unknown.
    """
    if settings is None:
        settings = load_settings()

    provider = settings.llm_provider.strip().lower()

    if provider == "deepseek":
        return _build_deepseek(settings)

    if provider == "mock":
        return MockChatModel()

    raise LLMFactoryError(
        f"Unknown LLM_PROVIDER '{settings.llm_provider}'. "
        "Supported values: deepseek, mock."
    )


def _build_deepseek(settings: Settings) -> BaseChatModel:
    """Build a ChatDeepSeek instance from settings.

    Imports lazily so the mock path never pulls in langchain-deepseek.
    """
    api_key = settings.deepseek_api_key

    # ── Validate API key ────────────────────────────────────
    if not api_key:
        msg = (
            "DEEPSEEK_API_KEY is missing. "
            "Add it to .env or export it in your shell.\n\n"
            "  echo 'DEEPSEEK_API_KEY=sk-your-key' >> .env\n\n"
            "If you just want to test without an API key, set:\n"
            "  LLM_PROVIDER=mock"
        )
        raise LLMFactoryError(msg)

    # ── Sanity check: not the placeholder ───────────────────
    if "your_deepseek_api_key_here" in api_key:
        raise LLMFactoryError(
            "DEEPSEEK_API_KEY is still set to the placeholder value "
            "from .env.example. Replace it with your actual API key in .env."
        )

    from langchain_deepseek import ChatDeepSeek

    return ChatDeepSeek(
        model=settings.deepseek_model,
        temperature=settings.deepseek_temperature,
        max_tokens=settings.deepseek_max_tokens,
        api_key=api_key,
    )
