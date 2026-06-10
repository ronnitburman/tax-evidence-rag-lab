"""Application settings loaded from environment variables.

Uses pydantic-settings for type-safe configuration with automatic env-var binding.
No secrets are ever hardcoded or logged.
"""

from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized, type-safe application settings.

    All values are read from environment variables or .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── Provider ──────────────────────────────────────────────
    llm_provider: str = "deepseek"

    # ── DeepSeek via LangChain ────────────────────────────────
    deepseek_api_key: str = ""
    deepseek_model: str = "deepseek-chat"
    deepseek_temperature: float = 0.0
    deepseek_max_tokens: int = 2048

    # ── LangSmith tracing (optional) ──────────────────────────
    langchain_tracing_v2: bool = False
    langchain_api_key: str = ""
    langchain_project: str = "tax-evidence-rag-lab"

    # ── Vector store ──────────────────────────────────────────
    chroma_persist_dir: str = "data/processed/chroma"

    # ── Retrieval defaults ────────────────────────────────────
    default_top_k: int = 5
    default_candidate_k: int = 30
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    # ── Project root (derived) ────────────────────────────────
    @property
    def project_root(self) -> Path:
        """Absolute path to the project root directory."""
        return Path(__file__).resolve().parent.parent.parent

    @property
    def chroma_persist_path(self) -> Path:
        """Absolute path to the Chroma persistence directory."""
        return self.project_root / self.chroma_persist_dir

    def masked_api_key(self) -> str:
        """Return a masked version of the API key for safe logging."""
        key = self.deepseek_api_key
        if not key:
            return "<not set>"
        if len(key) <= 8:
            return "*" * len(key)
        return key[:4] + "*" * (len(key) - 8) + key[-4:]


@lru_cache()
def load_settings() -> Settings:
    """Load and cache settings from environment/.env.

    Cached via lru_cache so the .env file is read only once.
    """
    return Settings()
