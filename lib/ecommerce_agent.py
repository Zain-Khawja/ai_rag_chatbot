# ecommerce_agent.py
from agno.agent import Agent
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.json import JSONKnowledgeBase
from agno.models.google import Gemini  # Google Gem
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
    embedder=embedder,  # Ensure the embedder is set here as well
    chunk_size=512,
    chunk_overlap=32
)

agent = Agent(
    model=Gemini(id="gemini-2.0-flash", api_key=api_key),
    knowledge=kb,
    search_knowledge=True,
    instructions=[
        "You are a helpful assistant for a safety and industrial product company.",
        "Use only the provided product data and static pages like About Us, Policies, Terms, etc.",
        "Answer clearly and politely with structured formatting:",
        "- Start with the title",
        "- Use bullet points for features",
        "- Include price, stock, SKU, category if available",
        "- Include refund, shipping or terms if relevant",
        "Do not make up data or hallucinate. Respond only with content from the knowledge base."
    ]
)

