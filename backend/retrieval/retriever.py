import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

with open("data/cleaned/netsol_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

index = faiss.read_index("data/cleaned/netsol.index")

def retrieve(query: str, top_k: int = 5):
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)
    
    results = []
    for i in indices[0]:
        if i < len(chunks):
            results.append(chunks[i])
    
    return results

def get_context_and_sources(query: str):
    results = retrieve(query, top_k=5)
    
    context = "\n\n".join([r["text"] for r in results])
    sources = list(set([r["url"] for r in results]))
    
    return context, sources