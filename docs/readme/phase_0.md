# Phase 0 — Commands & How to Run

> **Phase**: Project Scaffold with LangChain, DeepSeek, and LangGraph
>
> **Goal**: Repository structure, environment setup, dependency installation, and baseline CLI.

---

## Prerequisites

- Python 3.11+
- Git

---

## Initial Setup (One-Time)

These commands set up the project from scratch. Run them once at the start.

### 1. Clone the repo and enter the directory

```bash
git clone <repo-url>
cd tax-evidence-rag-lab
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows (PowerShell)
```

### 3. Install dependencies and register the CLI

```bash
pip install -e .
```

This does two things:
- Installs all dependencies from `requirements.txt`
- Registers the `tax-rag` CLI command on your PATH (editable mode — code changes reflect immediately)

### 4. Configure environment variables

```bash
cp .env.example .env
```

Then edit `.env` with your DeepSeek API key:

```bash
DEEPSEEK_API_KEY=sk-your-actual-key-here
```

> **Note**: The CLI runs without an API key in Phase 0 (it only prints configuration). The key will be needed starting in Phase 1.

---

## Phase 0 Commands

This phase provides **two modes**: CLI and API. Both call the same core logic.

---

## CLI Mode

There are **two ways** to invoke the CLI:

| Style | When to use | Example |
|-------|------------|---------|
| `tax-rag ask "..."` | After `pip install -e .` (recommended) | `tax-rag ask "question"` |
| `python -m cli.main ask "..."` | Dev quick-run without install | `python -m cli.main ask "question"` |

All commands below use the `tax-rag` style. Replace with `python -m cli.main` if you haven't installed.

---

### `tax-rag ask <QUESTION>`

**What it does**: Prints the received question, runtime configuration, and a reminder that the full RAG pipeline is not yet implemented.

```bash
tax-rag ask "What is input tax credit eligibility?"
```

**Expected output**:

```
───────────────────────────── TaxEvidence RAG Lab ──────────────────────────────

╭──────────── Your Question ────────────╮
│ What is input tax credit eligibility? │
╰───────────────────────────────────────╯

Runtime Configuration
  • LLM Provider : deepseek
  • Model        : deepseek-chat
  • Temperature  : 0.0
  • Max Tokens   : 2048
  • Top-K        : 5
  • Candidate-K  : 30
  • Chroma Dir   : data/processed/chroma
  • API Key      : <not set>

⚠  The LangGraph RAG pipeline is not yet implemented. This is the Phase 0
scaffold.
    Subsequent phases will add: ingestion → chunking → embeddings → retrieval →
reranking → generation → citation validation.
```

---

### `tax-rag ask <QUESTION> --model <MODEL>`

**What it does**: Same as above, but overrides the default LLM model via CLI flag.

```bash
tax-rag ask "What is input tax credit eligibility?" --model deepseek-chat
```

---

### `tax-rag ask <QUESTION> --top-k <N>`

**What it does**: Same as above, but overrides the number of evidence chunks to retrieve.

```bash
tax-rag ask "What is input tax credit eligibility?" --top-k 10
```

---

### `tax-rag ask <QUESTION> --model <MODEL> --top-k <N>`

**What it does**: Overrides both model and top-k simultaneously.

```bash
tax-rag ask "Are R&D expenses deductible?" --model deepseek-chat --top-k 7
```

---

### `tax-rag version`

**What it does**: Prints version information and exits.

```bash
tax-rag version
```

**Expected output**:

```
TaxEvidence RAG Lab v0.1.0
Phase 0 — Project Scaffold

Stack: LangChain + DeepSeek + LangGraph + ChromaDB
Status: Scaffold active, pipeline pending (Phases 1–13)
```

---

### `tax-rag --help`

**What it does**: Prints usage help with all available commands and options.

```bash
tax-rag --help
```

```
 Usage: tax-rag [OPTIONS] COMMAND [ARGS]...

 Ask questions against tax-evidence documents using RAG.

╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                      │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ ask      Ask a tax-evidence question using RAG.                              │
│ version  Print version information.                                          │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### `tax-rag ask --help`

**What it does**: Shows help for the `ask` subcommand (available options).

```bash
tax-rag ask --help
```

---

## API Mode

First, start the server:

```bash
uvicorn api.main:app --reload --port 8000
```

Then use any of these curl commands:

### `GET /health`

```bash
curl -s http://127.0.0.1:8000/health | python3 -m json.tool
```

**Expected output**:

```json
{
    "status": "ok",
    "phase": "0 — scaffold"
}
```

---

### `POST /ask` — Basic

```bash
curl -s -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is input tax credit eligibility?"}' \
  | python3 -m json.tool
```

**Expected output**:

```json
{
    "question": "What is input tax credit eligibility?",
    "answer": "[Phase 0 placeholder] The RAG pipeline is not yet implemented. Received question: 'What is input tax credit eligibility?'. Subsequent phases will add retrieval, reranking, generation, and citation validation.",
    "citations": [],
    "phase": "0 — scaffold"
}
```

---

### `POST /ask` — With Options

```bash
curl -s -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Are R&D expenses deductible?",
    "model": "deepseek-chat",
    "top_k": 7
  }' \
  | python3 -m json.tool
```

### API docs (Swagger UI)

Open in browser: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Dev Quick-Run (Without `pip install`)

If you haven't run `pip install -e .` yet, use `python -m` from the project root:

```bash
# Ask a question
python -m cli.main ask "What is input tax credit eligibility?"

# Version
python -m cli.main version

# Help
python -m cli.main --help
```

> **Why `cli.main`?** The `src/` directory is the package root (src-layout). So `src/cli/main.py` is importable as `cli.main`. The Typer app lives there with `ask` and `version` subcommands.

---

## Architecture Note

The CLI and API are separated from the core business logic. All three live at the same level under `src/`:

```
tax-rag ask "..." ──→ src/cli/main.py       ──→ src/core/ask.py
                         (Typer app)              (pure logic)
                     
python -m cli.main ──→ src/cli/main.py       ──→ src/core/ask.py
                         (same entry)             (same core)
                         
POST /ask ──────────→ src/api/routes/ask.py  ──→ src/core/ask.py
                         (placeholder)            (same core)
```

The core logic (`core/ask.py`) has zero dependencies on Typer or FastAPI — callable from CLI, API, or tests identically.

---

## Verification Checklist

Run all of these to confirm Phase 0 is working correctly:

- [ ] `tax-rag ask "test question"` — prints question + config + pipeline warning
- [ ] `tax-rag ask "test" --model deepseek-chat --top-k 10` — prints overridden config values
- [ ] `tax-rag version` — prints version, exits cleanly
- [ ] `tax-rag --help` — prints help text with `ask` and `version` subcommands
- [ ] `tax-rag ask --help` — prints help for the ask subcommand
- [ ] `python -m cli.main ask "test"` — works without pip install (dev quick-run)
- [ ] `python -m cli.main version` — works without pip install
- [ ] `uvicorn api.main:app --port 8000` — server starts, `/health` returns 200
- [ ] `curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d '{"question":"test"}'` — returns placeholder JSON
- [ ] `curl http://127.0.0.1:8000/docs` — Swagger UI returns 200

---

## Files Created/Changed in This Phase

| File | Status | Purpose |
|------|--------|---------|
| `requirements.txt` | NEW | Python dependencies |
| `pyproject.toml` | NEW | Project metadata, build config, console script (`tax-rag`) |
| `.env.example` | NEW | Environment variable template |
| `.gitignore` | NEW | Git ignore rules |
| `README.md` | NEW | Project overview |
| `src/config/settings.py` | NEW | Pydantic Settings configuration loader |
| `src/core/ask.py` | NEW | **Core ask logic** — pure function, no framework deps |
| `src/cli/main.py` | NEW | **Typer CLI** — `tax-rag ask` and `tax-rag version` |
| `src/api/main.py` | NEW | FastAPI app factory with CORS + routes |
| `src/api/routes/ask.py` | NEW | `POST /ask` endpoint with request/response models |
| `src/api/middleware/cors.py` | NEW | CORS middleware settings |
| `src/{ingest,chunking,embeddings,retrieval,generation,graph,eval}/__init__.py` | NEW | Placeholder packages for future phases |
| `docs/DESIGN_DECISIONS.md` | NEW | Design rationale per phase |
| `docs/CODE_FLOW.md` | NEW | Runtime code flow trace per phase |
| `docs/readme/phase_0.md` | NEW | This file — Phase 0 commands reference |
