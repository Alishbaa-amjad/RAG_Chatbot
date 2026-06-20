import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

with open("data/cleaned/netsol_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

index = faiss.read_index("data/cleaned/netsol.index")

def retrieve(query: str, top_k: int = 8):
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)

    results = []
    for i, dist in zip(indices[0], distances[0]):
        # Distance threshold — zyada door ke chunks reject karo
        if i < len(chunks) and dist < 2.5:
            results.append(chunks[i])

    return results

def get_context_and_sources(query: str):
    results = retrieve(query)

    if not results:
        return "", []

    context = "\n\n".join([r["text"] for r in results])
    sources = list(set([r["url"] for r in results]))

    return context, sources