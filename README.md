# TaxEvidence RAG Lab

**Evidence-backed RAG lab built with LangChain, DeepSeek, and LangGraph**

> ⚠️ **Disclaimer**: This project is a technical demonstration only. It does not provide real tax or legal advice. All content is synthetic or drawn from public educational sources.

## Overview

This project is a hands-on retrieval-augmented generation (RAG) lab inspired by tax/legal evidence workflows. It demonstrates production RAG thinking through an explicit, inspectable pipeline:

```text
documents → metadata → chunking → embeddings → retrieval
→ reranking → LangGraph agent flow → grounded answer
→ citation validation → evaluation
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM Client | LangChain DeepSeek |
| Orchestration | LangGraph |
| Vector Store | ChromaDB |
| Embeddings | Sentence Transformers |
| Lexical Retrieval | BM25 |
| Reranking | Cross-Encoder |
| CLI | Typer + Rich |
| Config | Pydantic Settings |

## Architecture

```
Raw Documents → Ingestion + Metadata → LangChain Documents
→ Chunking Strategies → Embeddings + Chroma
→ Dense + BM25 Retrieval → Hybrid + Filters
→ Cross-Encoder Reranking → LangGraph Agentic Flow
→ DeepSeek Grounded Generation → Citation Validation → Evaluation
```

## Quick Start

```bash
# Clone and set up
git clone <repo-url>
cd tax-evidence-rag-lab

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies and register the CLI
pip install -e .

# Configure environment
cp .env.example .env
# Edit .env with your DeepSeek API key

# Test the scaffold
tax-rag ask "What is input tax credit eligibility?"

# Or start the API server
uvicorn api.main:app --reload --port 8000
# Then: curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d '{"question": "..."}'
```

> **Dev tip**: Without installing, use `python -m cli.main ask "question"` for CLI or `uvicorn api.main:app` for API.

## Project Structure

```
tax-evidence-rag-lab/
├── src/
│   ├── config/       # Pydantic settings, env loading
│   ├── core/         # Pure business logic — no framework deps
│   ├── cli/          # Typer CLI — exposes `tax-rag` command
│   ├── api/          # FastAPI application (placeholder)
│   ├── ingest/       # Document ingestion pipeline
│   ├── chunking/     # Text splitting strategies
│   ├── embeddings/   # Embedding models and Chroma indexing
│   ├── retrieval/    # Dense, BM25, hybrid retrieval
│   ├── generation/   # Grounded answer generation
│   ├── graph/        # LangGraph agentic RAG flow
│   └── eval/         # Evaluation suite
├── data/             # Raw, processed, eval, and debug data
├── docs/             # Architecture docs, design decisions, code flow
├── notebooks/        # Exploratory notebooks
├── plans/            # Phase-by-phase build plans
└── scripts/          # Utility scripts
```

## Design Principles

1. **Provider isolation** — LLM configuration is centralized, not scattered
2. **Retrieval ≠ generation** — Evidence retrieval is kept separate from answer generation
3. **Metadata preservation** — Source metadata flows from ingestion through to citations
4. **Grounded answers** — Every claim must cite retrieved evidence
5. **Explicit state** — LangGraph makes the agentic flow inspectable
6. **Citation validation** — Post-generation guardrails verify evidence claims
7. **Separate evaluation** — Retrieval quality and answer quality are evaluated independently
8. **Visible uncertainty** — Missing information and low-confidence answers are surfaced

## License

MIT
