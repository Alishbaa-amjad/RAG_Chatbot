import json
import sqlite3
from datetime import datetime

def save_to_sqlite(cleaned_data):
    conn = sqlite3.connect("data/netsol.db")
    cursor = conn.cursor()

    # Table banao
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_url TEXT,
            page_title TEXT,
            cleaned_text TEXT,
            metadata TEXT,
            timestamp TEXT
        )
    ''')

    # Data insert karo
    for page in cleaned_data:
        metadata = json.dumps({
            "scraped_at": page["scraped_at"]
        })
        cursor.execute('''
            INSERT INTO documents 
            (source_url, page_title, cleaned_text, metadata, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            page["url"],
            page["title"],
            page["text"],
            metadata,
            datetime.now().isoformat()
        ))
        print(f"Stored: {page['url']}")

    conn.commit()
    conn.close()
    print("SQLite storage complete!")

def run_storage():
    with open("data/cleaned/netsol_cleaned.json", "r", encoding="utf-8") as f:
        cleaned_data = json.load(f)
    save_to_sqlite(cleaned_data)

if __name__ == "__main__":
    run_storage()