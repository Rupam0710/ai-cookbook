# Building a Knowledge Extraction Pipeline with Docling

A step-by-step RAG (Retrieval-Augmented Generation) pipeline that extracts knowledge from PDFs and web pages, chunks and embeds the content into a vector database, and serves it through a conversational chat interface powered by NVIDIA Nemotron.

---

## Pipeline Overview

```
PDF / HTML / Web
      │
      ▼
 1. Extraction       (Docling DocumentConverter)
      │
      ▼
 2. Chunking         (HybridChunker + NVIDIA Nemotron tokenizer)
      │
      ▼
 3. Embeddings       (NVIDIA NV-Embed-v2 → LanceDB)
      │
      ▼
 4. Search           (LanceDB vector search)
      │
      ▼
 5. Chat             (Streamlit + NVIDIA Nemotron 70B)
```

---

## File Structure

```
knowledge/docling/
├── 1-extraction.py       # Document extraction from PDF and web
├── 2-chunking.py         # Semantic chunking with tokenizer-aware splitting
├── 3-embeddings.py       # Embedding generation and vector store ingestion
├── 4-search.py           # Vector similarity search
├── 5-chat.py             # Streamlit RAG chat application
├── requirements.txt      # Python dependencies
├── .env                  # API keys (not committed)
├── data/
│   └── lancedb/          # Persisted vector database
└── utils/
    ├── sitemap.py        # Sitemap crawler utility
    └── tokenizer.py      # OpenAI-compatible tokenizer wrapper
```

---

## Step-by-Step Breakdown

### Step 1 — Document Extraction (`1-extraction.py`)

**Tool:** [`docling`](https://github.com/DS4SD/docling) — `DocumentConverter`

Docling converts raw documents (PDFs, HTML pages, DOCX, Markdown, etc.) into a structured internal representation that can be exported to Markdown or JSON.

**What it does:**
- Extracts a research paper from arXiv as a PDF (`2408.09869` — the Docling paper itself)
- Extracts content from the Docling website (`https://docling.ai/`)
- Scrapes all pages from a site by reading its `sitemap.xml` via `get_sitemap_urls()` and batch-converting with `converter.convert_all()`

**Key API:**
```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("https://arxiv.org/pdf/2408.09869")
markdown = result.document.export_to_markdown()
```

---

### Step 2 — Chunking (`2-chunking.py`)

**Tools:** `docling_core.HybridChunker`, `HuggingFaceTokenizer`, `transformers.AutoTokenizer`

Raw documents are too large to embed or send to an LLM directly. Chunking splits them into semantically coherent pieces that respect token limits.

**What it does:**
- Loads the NVIDIA Nemotron 70B tokenizer (`nvidia/Llama-3.1-Nemotron-70B-Instruct-HF`) to accurately count tokens as the target model sees them
- Wraps it in a `HuggingFaceTokenizer` compatible with Docling's chunker interface
- Uses `HybridChunker` which combines layout-aware splitting (headings, tables, lists) with token-limit enforcement (max 4096 tokens per chunk)
- `merge_peers=True` merges adjacent small chunks from the same section to reduce fragmentation

**Key API:**
```python
from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer

chunker = HybridChunker(tokenizer=tokenizer_wrapper, merge_peers=True)
chunks = list(chunker.chunk(dl_doc=result.document))
```

Each chunk carries rich metadata: `origin.filename`, `page_no` provenance, and `headings` for section context.

---

### Step 3 — Embeddings & Vector Store (`3-embeddings.py`)

**Tools:** `lancedb`, `nvidia/NV-Embed-v2` (fallback: `sentence-transformers/all-MiniLM-L6-v2`), `pydantic` schema via `LanceModel`

Chunks are converted into dense vector embeddings and stored in a local LanceDB vector database for fast semantic retrieval.

**What it does:**
- Connects to a local LanceDB instance at `data/lancedb`
- Attempts to load `nvidia/NV-Embed-v2` (a state-of-the-art embedding model) via LanceDB's HuggingFace registry; falls back to `all-MiniLM-L6-v2` if unavailable
- Defines a Pydantic schema (`Chunks`) with:
  - `text` — the chunk text (source field for embedding)
  - `vector` — the auto-generated embedding vector
  - `metadata` — structured metadata (`filename`, `page_numbers`, `title`)
- Processes all chunks and inserts them into the `docling` table; LanceDB automatically calls the embedding function on insert

**Key API:**
```python
import lancedb
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector

func = (
    get_registry()
    .get("huggingface")
    .create(name="nvidia/NV-Embed-v2", trust_remote_code=True)
)


class Chunks(LanceModel):
    text: str = func.SourceField()
    vector: Vector(func.ndims()) = func.VectorField()
    metadata: ChunkMetadata


table = db.create_table("docling", schema=Chunks, mode="overwrite")
table.add(processed_chunks)  # embeddings generated automatically
```

---

### Step 4 — Vector Search (`4-search.py`)

**Tool:** `lancedb` — vector similarity search

Demonstrates querying the vector database directly to verify retrieval quality before wiring it into a chat interface.

**What it does:**
- Opens the persisted `docling` table from `data/lancedb`
- Runs a natural language vector search using cosine similarity
- Returns the top-3 most semantically relevant chunks as a Pandas DataFrame

**Key API:**
```python
result = table.search(query="what's docling?", query_type="vector").limit(3)
result.to_pandas()
```

---

### Step 5 — RAG Chat Application (`5-chat.py`)

**Tools:** `streamlit`, NVIDIA NIM API (`nvidia/llama-3.1-nemotron-70b-instruct`), `lancedb`, `python-dotenv`

A full conversational chat interface that ties the entire pipeline together using Retrieval-Augmented Generation.

**What it does:**
1. Loads `NVIDIA_API_KEY` / `NEMOTRON_API_KEY` from `.env` (path resolved relative to the script using `Path(__file__).parent`)
2. Initialises an OpenAI-compatible client pointed at NVIDIA NIM (`https://integrate.api.nvidia.com/v1`)
3. On each user message:
   - Searches LanceDB for the 5 most relevant chunks (`get_context`)
   - Displays retrieved sources in collapsible UI cards with filename and page citations
   - Injects the retrieved context into a system prompt and streams the model response
4. Maintains full multi-turn chat history in `st.session_state`

**Model:** `nvidia/llama-3.1-nemotron-70b-instruct` via NVIDIA NIM (free tier)

**Key API:**
```python
stream = client.chat.completions.create(
    model="nvidia/llama-3.1-nemotron-70b-instruct",
    messages=[{"role": "system", "content": system_prompt_with_context}, *messages],
    temperature=0.7,
    stream=True,
)
response = st.write_stream(stream)
```

---

## Utility Modules

### `utils/sitemap.py`
Fetches and parses a website's `sitemap.xml` to extract all page URLs. Used in Step 1 for bulk web scraping. Returns just the base URL if no sitemap exists (404 fallback).

### `utils/tokenizer.py`
A `PreTrainedTokenizerBase` wrapper around OpenAI's `tiktoken` (`cl100k_base` encoding). Makes OpenAI-style tokenizers compatible with Docling's `HybridChunker` interface, which expects a HuggingFace tokenizer signature.

---

## Setup

### 1. Install dependencies

```bash
pip install docling docling-core lancedb transformers sentence-transformers \
            streamlit openai python-dotenv tiktoken requests
```

### 2. Configure API keys

Create `knowledge/docling/.env`:

```env
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxx
```

Get your free NVIDIA NIM API key at [build.nvidia.com](https://build.nvidia.com).

### 3. Run the pipeline in order

```bash
cd knowledge/docling

python 1-extraction.py    # verify extraction works
python 2-chunking.py      # verify chunking output
python 3-embeddings.py    # builds the vector database (takes a few minutes)
python 4-search.py        # verify retrieval is working
streamlit run 5-chat.py   # launch the chat app
```

---

## Key Technologies

| Tool | Role |
|------|------|
| [Docling](https://github.com/DS4SD/docling) | PDF/HTML/web document extraction and parsing |
| `HybridChunker` | Layout-aware + token-aware document chunking |
| `nvidia/Llama-3.1-Nemotron-70B-Instruct-HF` | Tokenizer for accurate chunk token counting |
| `nvidia/NV-Embed-v2` | High-quality text embeddings |
| `sentence-transformers/all-MiniLM-L6-v2` | Fallback local embedding model |
| [LanceDB](https://lancedb.github.io/lancedb/) | Local serverless vector database |
| [NVIDIA NIM](https://build.nvidia.com) | Hosted inference API for Nemotron 70B |
| [Streamlit](https://streamlit.io) | Chat UI framework |
| `python-dotenv` | Environment variable management |
