import os

import lancedb
from docling.document_converter import DocumentConverter
from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
from dotenv import load_dotenv
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from transformers import AutoTokenizer

load_dotenv()

# Avoid TorchInductor compiler issues on Windows machines without MSVC build tools.
os.environ.setdefault("TORCHDYNAMO_DISABLE", "1")

# Chunking tokenizer (NVIDIA Nemotron)
NEMOTRON_TOKENIZER = "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF"
CHUNK_MAX_TOKENS = 4096

tokenizer = AutoTokenizer.from_pretrained(NEMOTRON_TOKENIZER)
tokenizer_wrapper = HuggingFaceTokenizer(
    tokenizer=tokenizer,
    max_tokens=CHUNK_MAX_TOKENS,
)


# --------------------------------------------------------------
# Extract the data
# --------------------------------------------------------------

converter = DocumentConverter()
result = converter.convert("https://arxiv.org/pdf/2408.09869")


# --------------------------------------------------------------
# Apply hybrid chunking
# --------------------------------------------------------------

chunker = HybridChunker(
    tokenizer=tokenizer_wrapper,
    merge_peers=True,
)

chunk_iter = chunker.chunk(dl_doc=result.document)
chunks = list(chunk_iter)

chunks[0].model_dump()

# --------------------------------------------------------------
# Create a LanceDB database and table
# --------------------------------------------------------------

# Create a LanceDB database
db = lancedb.connect("data/lancedb")


def build_embedding_function():
    """Create an embedding function with NVIDIA-first strategy.

    NV-Embed-v2 can fail on some transformers/runtime combinations, so we
    gracefully fall back to a stable local model when needed.
    """
    try:
        return (
            get_registry()
            .get("huggingface")
            .create(
                name="nvidia/NV-Embed-v2",
                trust_remote_code=True,
            )
        )
    except Exception as exc:
        print(
            "Warning: NV-Embed-v2 unavailable in current environment. "
            f"Falling back to all-MiniLM-L6-v2. Details: {exc}"
        )
        return (
            get_registry()
            .get("huggingface")
            .create(name="sentence-transformers/all-MiniLM-L6-v2")
        )


func = build_embedding_function()


# Define a simplified metadata schema
class ChunkMetadata(LanceModel):
    """
    You must order the fields in alphabetical order.
    This is a requirement of the Pydantic implementation.
    """

    filename: str | None
    page_numbers: list[int] | None
    title: str | None


# Define the main Schema
class Chunks(LanceModel):
    text: str = func.SourceField()
    vector: Vector(func.ndims()) = func.VectorField()  # type: ignore
    metadata: ChunkMetadata


table = db.create_table("docling", schema=Chunks, mode="overwrite")

# --------------------------------------------------------------
# Prepare the chunks for the table
# --------------------------------------------------------------

# Create table with processed chunks
processed_chunks = [
    {
        "text": chunk.text,
        "metadata": {
            "filename": chunk.meta.origin.filename,
            "page_numbers": [
                page_no
                for page_no in sorted(
                    {
                        prov.page_no
                        for item in chunk.meta.doc_items
                        for prov in item.prov
                    }
                )
            ]
            or None,
            "title": chunk.meta.headings[0] if chunk.meta.headings else None,
        },
    }
    for chunk in chunks
]

# --------------------------------------------------------------
# Add the chunks to the table (automatically embeds the text)
# --------------------------------------------------------------

table.add(processed_chunks)

# --------------------------------------------------------------
# Load the table
# --------------------------------------------------------------

table.to_pandas()
table.count_rows()
