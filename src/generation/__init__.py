"""Grounded answer generation — LLM factory and mock client."""

from generation.llm_factory import LLMFactoryError, get_chat_model
from generation.mock_llm import MockChatModel

__all__ = ["get_chat_model", "MockChatModel", "LLMFactoryError"]
