import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from datetime import datetime

def run_chunker():
    with open("data/cleaned/netsol_cleaned.json", "r", encoding="utf-8") as f:
        cleaned_data = json.load(f)

    # LangChain ka RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    # LangChain Documents banao
    documents = []
    for page in cleaned_data:
        doc = Document(
            page_content=page["text"],
            metadata={
                "url": page["url"],
                "title": page["title"],
                "scraped_at": page["scraped_at"]
            }
        )
        documents.append(doc)

    # Split karo
    chunks = splitter.split_documents(documents)
    print(f"Total chunks: {len(chunks)}")

    # Structured format mein save karo
    all_chunks = []
    for i, chunk in enumerate(chunks):
        all_chunks.append({
            "id": i,
            "text": chunk.page_content,
            "url": chunk.metadata["url"],
            "title": chunk.metadata["title"],
            "scraped_at": chunk.metadata["scraped_at"],
            "chunk_index": i,
            "timestamp": datetime.now().isoformat()
        })
        print(f"Chunk {i} — {len(chunk.page_content)} chars — {chunk.metadata['url']}")

    with open("data/cleaned/netsol_chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"\nDone! {len(all_chunks)} chunks saved!")
    return all_chunks

if __name__ == "__main__":
    run_chunker()