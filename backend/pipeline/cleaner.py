import json
import re

def clean_text(text):
    # Cookie text hatao
    cookie_pattern = r'This website uses cookies.*?Allow all'
    text = re.sub(cookie_pattern, '', text, flags=re.DOTALL)
    
    # Navigation/footer common text hatao
    nav_texts = [
        "Terms of Use", "Privacy Policy", "Human Rights Policy",
        "Modern Slavery Act", "Subscribe to our newsletter",
        "Connect With Us", "All Rights Reserved",
        "Consent Selection", "Necessary Preferences Statistics Marketing",
        "Show details", "Deny", "Allow selection"
    ]
    for nav in nav_texts:
        text = text.replace(nav, '')
    
    # Extra spaces aur lines hatao
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    text = text.strip()
    
    return text

def run_cleaner():
    with open("data/raw/netsol_raw.json", "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    cleaned = []
    for page in raw_data:
        cleaned_text = clean_text(page["text"])
        cleaned.append({
            "url": page["url"],
            "title": page["title"],
            "text": cleaned_text,
            "scraped_at": page["scraped_at"]
        })
        print(f"Cleaned: {page['url']} — {len(cleaned_text)} chars")

    with open("data/cleaned/netsol_cleaned.json", "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    print(f"Done! {len(cleaned)} pages cleaned!")

if __name__ == "__main__":
    run_cleaner()