import json

def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # Overlap rakho
    
    return chunks

def run_chunker():
    with open("data/cleaned/netsol_cleaned.json", "r", encoding="utf-8") as f:
        cleaned_data = json.load(f)

    all_chunks = []
    chunk_id = 0

    for page in cleaned_data:
        chunks = chunk_text(page["text"])
        
        for chunk in chunks:
            all_chunks.append({
                "id": chunk_id,
                "text": chunk,
                "url": page["url"],
                "title": page["title"]
            })
            chunk_id += 1

        print(f"✅ {page['url']} — {len(chunks)} chunks")

    with open("data/cleaned/netsol_chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Total {len(all_chunks)} chunks!")
    return all_chunks

if __name__ == "__main__":
    run_chunker()