#checking.py
from agno.vectordb.pgvector import PgVector
from agno.embedder.fastembed import FastEmbedEmbedder
from lib.config import PGVECTOR_DB_URL

embedder = FastEmbedEmbedder()
vector_db = PgVector(
    table_name="products",
    db_url=PGVECTOR_DB_URL,
    schema="public",
    embedder=embedder,
)

results = vector_db.search("tell me about your company")
for r in results:
    print(r.content[:300])  # Use .content instead of ['content']
