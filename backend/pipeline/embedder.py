import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def run_embedder():
    # Chunks load karo
    with open("data/cleaned/netsol_chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print("Model is loading...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Embeddings banao
    texts = [chunk["text"] for chunk in chunks]
    print(f"Embeddings ban rahi hain {len(texts)} chunks ki...")
    embeddings = model.encode(texts, show_progress_bar=True)

    # FAISS index banao
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    # Save karo
    faiss.write_index(index, "data/cleaned/netsol.index")
    
    with open("data/cleaned/netsol_chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"Done! {index.ntotal} embeddings saved!")

if __name__ == "__main__":
    run_embedder()