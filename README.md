# AI Cookbook

**AI Cookbook** is a practical, code-first learning repository for AI engineers and developers. It provides self-contained, runnable recipes that demonstrate how to build real-world AI applications — from querying large language models to constructing full retrieval-augmented generation (RAG) pipelines and designing autonomous agents.

Each recipe is structured progressively: starting with the fundamentals and building toward production-ready patterns.

---

## Repository Structure

```
ai-cookbook/
├── models/
│   └── responses/              # OpenAI Responses API examples (01–08)
├── knowledge/
│   └── docling/                # Knowledge extraction & RAG pipeline (1–5)
├── agents/
│   └── building-blocks/        # 7 building blocks for reliable AI agents (1–7)
├── patterns/
│   └── workflows/              # LLM workflow patterns — intro + 4 patterns (1–4)
└── building_effective_agents/  # Agentic patterns guide (Anthropic)
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

## 3. Building Effective Agents

> **Location:** `building_effective_agents/`  
> Based on [Anthropic's engineering guide](https://www.anthropic.com/engineering/building-effective-agents)

A comprehensive reference guide covering every agentic pattern used in production LLM systems — with Mermaid diagrams and runnable Python examples for each pattern.

### Patterns Covered

| Pattern | Description | When to use |
|---------|-------------|-------------|
| **Augmented LLM** | LLM + retrieval + tools + memory | Foundation of all agentic systems |
| **Prompt Chaining** | Sequential steps with gate checks | Fixed, decomposable tasks |
| **Routing** | Classify input → specialist handler | Distinct input categories |
| **Parallelization** | Simultaneous independent subtasks | Speed or confidence via voting |
| **Orchestrator-Workers** | Central LLM delegates dynamically | Unpredictable subtasks |
| **Evaluator-Optimizer** | Generate → evaluate → refine loop | Quality-critical outputs |
| **Autonomous Agents** | LLM in a tool-use loop | Open-ended, multi-step tasks |

### Decision Guide

```
Start simple → add complexity only when needed

Single LLM call → Prompt Chain → Routing → Parallelization
→ Orchestrator-Workers → Evaluator-Optimizer → Autonomous Agent
```

See [`building_effective_agents/README.md`](building_effective_agents/README.md) for the full guide with diagrams and code examples.

---

## 4. 7 Building Blocks for Reliable AI Agents

> **Location:** `agents/building-blocks/`

Seven self-contained Python scripts, each demonstrating one essential building block that every production AI agent needs. Each file is runnable independently.

### The Building Blocks

| # | Block | File | What it does |
|---|-------|------|--------------|
| 1 | 🧠 Intelligence | `1-intelligence.py` | LLM processes input and generates a response |
| 2 | 💾 Memory | `2-memory.py` | Pass full chat history to maintain context across turns |
| 3 | 🔧 Tools | `3-tools.py` | LLM calls your functions to act in the real world |
| 4 | ✅ Validation | `4-validation.py` | Pydantic schema enforces structured, typed output |
| 5 | 🔀 Control | `5-control.py` | If/then routing based on classified user intent |
| 6 | 🛡️ Recovery | `6-recovery.py` | Try/except + fallbacks for graceful failure handling |
| 7 | 👤 Feedback | `7-feedback.py` | Human approval gate for high-stakes actions |

### How they connect

```
User Input
   → 🧠 Intelligence  (understands the task)
   → 💾 Memory        (retrieves past context)
   → 🔧 Tools         (calls external APIs)
   → ✅ Validation    (ensures correct output format)
   → 🔀 Control       (routes to the right handler)
   → 🛡️ Recovery      (handles errors & edge cases)
   → 👤 Feedback      (human approves if needed)
   → Response
```

See [`agents/building-blocks/README.md`](agents/building-blocks/README.md) for diagrams and full explanations.

---

## 5. LLM Workflow Patterns

> **Location:** `patterns/workflows/`

A hands-on guide to the most common LLM workflow patterns, built progressively from a single API call up to a full orchestrator-workers system.

### Part 1 — Core Building Blocks

| File | What it covers |
|------|----------------|
| `1-introduction/1-basic.py` | Plain text completion — the simplest LLM call |
| `1-introduction/2-structurred.py` | Pydantic structured output — typed, validated responses |
| `1-introduction/3-tools.py` | Function calling — LLM triggers your Python functions |
| `1-introduction/4-retrieval.py` | RAG — LLM answers from your private knowledge base |

### Part 2 — Workflow Patterns

| Pattern | File | When to use |
|---------|------|-------------|
| **Prompt Chaining** | `2-workflow-patterns/1-prompt-chaining.py` | Fixed multi-step task with quality gate checks |
| **Routing** | `2-workflow-patterns/2-routing.py` | Different input types need different specialised handlers |
| **Parallelization** | `2-workflow-patterns/3-parallization.py` | Independent checks that run simultaneously |
| **Orchestrator-Workers** | `2-workflow-patterns/4-orchestrator.py` | Dynamic tasks where number of steps is unknown |

### How complexity grows

```
Basic → Structured → Tools/Retrieval
                         │
              ┌──────────┼──────────┐
         Chaining    Routing   Parallelization
              └──────────┼──────────┘
                         │
                Orchestrator-Workers
```

See [`patterns/workflows/README.md`](patterns/workflows/README.md) for full diagrams and explanations.

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
| `openai` | Responses API examples, agent patterns |
| `anthropic` | Building effective agents examples |
| `groq` | Alternative LLM provider |
| `docling` / `docling-core` | Document extraction & chunking |
| `lancedb` | Vector database |
| `transformers` | Tokenizers and embedding models |
| `streamlit` | Chat UI |
| `python-dotenv` | Environment variable loading |
| `pypdf` | PDF utilities |
