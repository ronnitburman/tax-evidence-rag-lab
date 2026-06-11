# Phase 1 — Commands & How to Run

> **Phase**: LangChain DeepSeek Client and Configuration
>
> **Goal**: LLM factory with LangChain DeepSeek integration, mock fallback, and error handling.

---

## Prerequisites

- Phase 0 completed (`pip install -e .` done, `tax-rag` available)
- (Optional) DeepSeek API key for live testing

---

## New Files

| File | Purpose |
|------|---------|
| `src/generation/llm_factory.py` | `get_chat_model()` — returns `ChatDeepSeek` or `MockChatModel` |
| `src/generation/mock_llm.py` | `MockChatModel` — fake LLM for tests/offline dev |
| `scripts/test_deepseek_langchain.py` | Integration test script for the LLM factory |

---

## Phase 1 Commands

### Mock Mode (No API Key Required)

Test the LLM pipeline without any API key:

```bash
# CLI
LLM_PROVIDER=mock tax-rag ask "What is input tax credit eligibility?"

# Integration test script
LLM_PROVIDER=mock python scripts/test_deepseek_langchain.py

# API (start server first with mock)
LLM_PROVIDER=mock uvicorn api.main:app --port 8000
# Then: curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d '{"question":"test"}'
```

**Expected output (CLI)**:

```
───────────────────────────── TaxEvidence RAG Lab ──────────────────────────────

╭──────────── Your Question ────────────╮
│ What is input tax credit eligibility? │
╰───────────────────────────────────────╯

Runtime Configuration
  • LLM Provider : mock
  • Model        : deepseek-chat
  • Temperature  : 0.0
  • Max Tokens   : 2048
  • Top-K        : 5
  • Candidate-K  : 30
  • Chroma Dir   : data/processed/chroma
  • API Key      : <not set>

LLM Response
╭──────────────────────────── mock / deepseek-chat ────────────────────────────╮
│ [MOCK LLM — LLM_PROVIDER=mock is active]                                     │
│                                                                              │
│ You asked: "What is input tax credit eligibility?"                           │
│                                                                              │
│ This is a mock response. Set LLM_PROVIDER=deepseek and add a                 │
│ DEEPSEEK_API_KEY to .env for real answers.                                   │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### Real DeepSeek Mode (API Key Required)

First, configure your API key:

```bash
cp .env.example .env
# Edit .env: DEEPSEEK_API_KEY=sk-your-actual-key
```

Then test:

```bash
# CLI
tax-rag ask "What is input tax credit eligibility?"

# Integration test script
python scripts/test_deepseek_langchain.py

# API
uvicorn api.main:app --port 8000
curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d '{"question":"What is input tax credit eligibility?"}'
```

---

### `scripts/test_deepseek_langchain.py`

**What it does**: Standalone integration test — loads settings, creates the model via factory, sends a test prompt, verifies the response.

```bash
# With mock (no API key)
LLM_PROVIDER=mock python scripts/test_deepseek_langchain.py

# With DeepSeek (API key required)
python scripts/test_deepseek_langchain.py
```

**Expected output (mock)**:

```
──────────────────── LangChain DeepSeek — Integration Test ─────────────────────

1. Loading settings...
   Provider : mock
   Model    : deepseek-chat
   API Key  : <not set>

2. Creating chat model via factory...
   ✓ Model created: MockChatModel

3. Sending test prompt...

╭─────────────────────────────── Model Response ───────────────────────────────╮
│ [MOCK LLM — LLM_PROVIDER=mock is active]                                     │
│ ...                                                                          │
╰──────────────────────────────────────────────────────────────────────────────╯

4. Verifying response...
   ✓ Response contains expected keywords.

───────────────────────────────── Test Passed ──────────────────────────────────
```

---

### Error: Missing API Key

If `LLM_PROVIDER=deepseek` but no API key is set:

```bash
tax-rag ask "test"
```

**Expected output**:

```
LLM Response
╭─────────────────────────────── LLM Error ────────────────────────────────────╮
│ DEEPSEEK_API_KEY is missing. Add it to .env or export it in your shell.      │
│                                                                              │
│   echo 'DEEPSEEK_API_KEY=sk-your-key' >> .env                                │
│                                                                              │
│ If you just want to test without an API key, set:                            │
│   LLM_PROVIDER=mock                                                          │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### Error: Placeholder API Key

If `.env` still has the `.env.example` placeholder:

```bash
# .env contains: DEEPSEEK_API_KEY=your_deepseek_api_key_here
tax-rag ask "test"
```

**Expected output**:

```
DEEPSEEK_API_KEY is still set to the placeholder value from .env.example.
Replace it with your actual API key in .env.
```

---

## Verification Checklist

- [ ] `LLM_PROVIDER=mock tax-rag ask "test"` — mock response with `[MOCK LLM]` prefix
- [ ] `LLM_PROVIDER=mock python scripts/test_deepseek_langchain.py` — test passes (mock)
- [ ] `tax-rag ask "test"` (no API key, default deepseek) — helpful error message shown
- [ ] `tax-rag ask "test"` (with real API key) — DeepSeek responds (if key available)
- [ ] `python scripts/test_deepseek_langchain.py` (with real API key) — test passes (if key available)
- [ ] API with mock: `LLM_PROVIDER=mock uvicorn api.main:app` + curl /ask — returns mock response
- [ ] No API key is ever printed in logs or error messages (only masked version)

---

## Design Notes

### Provider isolation

The entire project uses `get_chat_model()`, never `ChatDeepSeek(...)` directly. To switch from DeepSeek to another provider (e.g., OpenAI, Anthropic), you change one function in `llm_factory.py` — nothing else.

### Mock for offline/test

Setting `LLM_PROVIDER=mock` activates `MockChatModel`, a `BaseChatModel` subclass that returns deterministic responses. This means:
- CI/CD pipelines run without API keys
- Unit tests have predictable output
- Offline development works immediately

### Lazy import

`langchain-deepseek` is imported inside `_build_deepseek()`, not at module level. This means `LLM_PROVIDER=mock` never loads the DeepSeek SDK — faster startup, fewer dependencies.
