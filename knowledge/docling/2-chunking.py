import os

from docling.document_converter import DocumentConverter
from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
from dotenv import load_dotenv
from transformers import AutoTokenizer

load_dotenv()

# Avoid TorchInductor compiler issues on Windows machines without MSVC build tools.
os.environ.setdefault("TORCHDYNAMO_DISABLE", "1")

# NVIDIA Nemotron 3 Ultra tokenizer settings
NEMOTRON_TOKENIZER = "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF"
MAX_TOKENS = 4096

tokenizer = AutoTokenizer.from_pretrained(NEMOTRON_TOKENIZER)
tokenizer_wrapper = HuggingFaceTokenizer(tokenizer=tokenizer, max_tokens=MAX_TOKENS)


# --------------------------------------------------------------
# Extract the data
# --------------------------------------------------------------

converter = DocumentConverter()

# You can pass a local file path (pdf, md, docx, etc.) or a URL.
source = "https://arxiv.org/pdf/2408.09869"
result = converter.convert(source)


# --------------------------------------------------------------
# Apply hybrid chunking
# --------------------------------------------------------------

chunker = HybridChunker(
    tokenizer=tokenizer_wrapper,
    merge_peers=True,
)

chunk_iter = chunker.chunk(dl_doc=result.document)
chunks = list(chunk_iter)

len(chunks)
