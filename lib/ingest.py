# ingest.py
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.json import JSONKnowledgeBase
from agno.embedder.google import GeminiEmbedder  # Google Gemini embedder
from lib.config import GEMINI_API_KEY
import os

# Use absolute paths to ensure consistent behavior
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
chroma_data_path = os.path.join(base_dir, "chroma_data")
woocommerce_data_path = os.path.join(base_dir, "knowledge_base.json")

api_key = GEMINI_API_KEY
embedder = GeminiEmbedder(api_key=api_key)

vector_db = ChromaDb(
    path=chroma_data_path,
    embedder=embedder,
    collection="woocommerce_knowledge",
    persistent_client=True
)

kb = JSONKnowledgeBase(
    path=woocommerce_data_path,
    vector_db=vector_db,
    embedder=embedder,
    chunk_size=512,
    chunk_overlap=32
)

kb.load()
