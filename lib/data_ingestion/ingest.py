import sys, os, glob, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from agno.vectordb.pgvector import PgVector
from agno.embedder.fastembed import FastEmbedEmbedder
from agno.knowledge.json import JSONKnowledgeBase
from lib.config import PGVECTOR_DB_URL

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
json_batches_path = os.path.join(base_dir, "data", "json_batches")

embedder = FastEmbedEmbedder()
vector_db = PgVector(
    table_name="products",
    schema="public",
    db_url=PGVECTOR_DB_URL,
    embedder=embedder,
)

batch_files = sorted(glob.glob(os.path.join(json_batches_path, "batch_*.json")))
print("Ingesting data into vector database...")

for i, batch_file in enumerate(batch_files):
    print(f"Processing {os.path.basename(batch_file)} ({i+1}/{len(batch_files)})")
    print(f"\n Processing {os.path.basename(batch_file)} ({i+1}/{len(batch_files)})")

    kb = JSONKnowledgeBase(
        path=batch_file,
        vector_db=vector_db,
        embedder=embedder,
        chunk_size=256,
        chunk_overlap=16
    )

    for retry in range(3):
        try:
            kb.load()
            print(f" Success: {os.path.basename(batch_file)}")
            break
        except Exception as e:
            print(f" Retry {retry + 1}/3 failed for {os.path.basename(batch_file)}: {e}")
            wait = 30 * (retry + 1)
            print(f" Waiting {wait} seconds before retry...")
            time.sleep(wait)
    else:
        print(f" Giving up on {os.path.basename(batch_file)} after 3 attempts")
