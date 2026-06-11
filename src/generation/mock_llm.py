"""Mock chat model — fake LLM for offline development and tests.

Implements the BaseChatModel interface with predictable, no-API responses.
"""

from __future__ import annotations

from typing import Any, Sequence

from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult


class MockChatModel(BaseChatModel):
    """A fake chat model that returns deterministic responses.

    Useful for:
    - Offline development (no API key needed)
    - Unit tests (predictable output)
    - CI/CD pipelines (no network dependency)

    Set LLM_PROVIDER=mock in .env to activate.
    """

    model_name: str = "mock-chat-v0"

    @property
    def _llm_type(self) -> str:
        return "mock-chat"

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: Sequence[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Return a deterministic mock response.

        Echoes the last user message content with a [MOCK] prefix so
        the caller can verify the mock is active.
        """
        last_user = ""
        for msg in reversed(messages):
            if hasattr(msg, "content") and msg.type == "human":
                last_user = str(msg.content)
                break

        response_text = (
            f'[MOCK LLM — LLM_PROVIDER=mock is active]\n\n'
            f'You asked: "{last_user}"\n\n'
            f'This is a mock response. Set LLM_PROVIDER=deepseek '
            f'and add a DEEPSEEK_API_KEY to .env for real answers.'
        )

        return ChatResult(
            generations=[
                ChatGeneration(
                    message=AIMessage(content=response_text),
                )
            ]
        )

    @property
    def _identifying_params(self) -> dict[str, Any]:
        return {"model_name": self.model_name}
