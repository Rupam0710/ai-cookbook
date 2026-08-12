# AI Cookbook

A collection of hands-on AI engineering recipes covering LLM APIs, RAG pipelines, document extraction, and conversational AI — built with Python.

---

## Repository Structure

```
ai-cookbook/
├── models/
│   └── responses/          # OpenAI Responses API examples (01–08)
└── knowledge/
    └── docling/            # Knowledge extraction & RAG pipeline (1–5)
```

---

## 1. OpenAI Responses API

> **Location:** `models/responses/`

A progressive walkthrough of the OpenAI Responses API — from basic text prompting through to reasoning, file search, and web-grounded responses.

### Topics Covered

| File | Topic |
|------|-------|
| `01-introduction.py` | Responses API vs Chat Completions, image input, streaming |
| `02-text-prompting.py` | System/user roles, prompt engineering basics |
| `03-conversation-state.py` | Multi-turn conversation and state management |
| `04-function-calling.py` | Defining and invoking custom tools/functions |
| `05-structured-output.py` | JSON schema-constrained model output |
| `06-web-search.py` | Grounding responses with live web search |
| `07-file-search.py` | Querying uploaded files / vector stores |
| `08-reasoning.py` | Working with o-series reasoning models |

### Key Concepts

- **Backward Compatibility** — The Responses API is a superset of Chat Completions. Everything possible with Chat Completions works with Responses API, plus additional features.
- **Built-in Tools** — Web search, file search, computer use, and function calling are all first-class citizens.
- **Simplified State** — Conversation state management that previously required manual message list wrangling is now handled natively.
- **Reasoning Models** — Improved support for o-series models with dedicated reasoning configuration.

### Resources

- [Responses API Docs](https://platform.openai.com/docs/api-reference/responses)
- [OpenAI Agents SDK](https://platform.openai.com/docs/guides/agents)

---

## 2. Knowledge Extraction Pipeline with Docling

> **Location:** `knowledge/docling/`

A full end-to-end RAG (Retrieval-Augmented Generation) pipeline that extracts knowledge from PDFs and websites, chunks and embeds content into a vector database, and serves it via a streaming chat interface.

### Pipeline

```
PDF / HTML / Web
      │
      ▼
 1-extraction.py     →  Docling DocumentConverter
      │
      ▼
 2-chunking.py       →  HybridChunker + NVIDIA Nemotron tokenizer
      │
      ▼
 3-embeddings.py     →  NVIDIA NV-Embed-v2 → LanceDB vector store
      │
      ▼
 4-search.py         →  LanceDB vector similarity search
      │
      ▼
 5-chat.py           →  Streamlit + NVIDIA Nemotron 70B (RAG chat)
```

### Steps

| File | Tool / Model | What it does |
|------|-------------|--------------|
| `1-extraction.py` | `docling.DocumentConverter` | Converts PDFs and web pages to structured Markdown/JSON |
| `2-chunking.py` | `HybridChunker`, Nemotron tokenizer | Splits documents into semantically coherent, token-bounded chunks |
| `3-embeddings.py` | `nvidia/NV-Embed-v2`, LanceDB | Embeds chunks and stores them in a local vector database |
| `4-search.py` | LanceDB vector search | Verifies retrieval quality with natural language queries |
| `5-chat.py` | Streamlit, NVIDIA NIM | Full RAG chat app with source citations and streaming |

### Tech Stack

| Tool | Role |
|------|------|
| [Docling](https://github.com/DS4SD/docling) | PDF/HTML/web document parsing |
| `HybridChunker` | Layout-aware + token-aware chunking |
| `nvidia/NV-Embed-v2` | Text embeddings |
| [LanceDB](https://lancedb.github.io/lancedb/) | Local serverless vector database |
| [NVIDIA NIM](https://build.nvidia.com) | Hosted `llama-3.1-nemotron-70b-instruct` inference |
| [Streamlit](https://streamlit.io) | Chat UI |

See [`knowledge/docling/README.md`](knowledge/docling/README.md) for full setup and usage instructions.

---

## Getting Started

### Prerequisites

- Python ≥ 3.13
- API keys for OpenAI and/or NVIDIA NIM

### Install

```bash
pip install -e .
```

### Environment

Create a `.env` file in the relevant subfolder:

```env
# For models/responses/
OPENAI_API_KEY=sk-...

# For knowledge/docling/
NVIDIA_API_KEY=nvapi-...
```

---

## Dependencies

| Package | Used by |
|---------|---------|
| `openai` | Responses API examples |
| `groq` | Alternative LLM provider |
| `docling` / `docling-core` | Document extraction & chunking |
| `lancedb` | Vector database |
| `transformers` | Tokenizers and embedding models |
| `streamlit` | Chat UI |
| `python-dotenv` | Environment variable loading |
| `pypdf` | PDF utilities |
