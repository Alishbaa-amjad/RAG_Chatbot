import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

PAGES = [
    "https://netsoltech.com/",
    "https://netsoltech.com/about-us",
    "https://netsoltech.com/services",
    "https://netsoltech.com/products",
]
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")        # Browser window mat kholo
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver

def scrape_page(driver, url):
    try:
        print(f"Scraping: {url}")
        driver.get(url)
        time.sleep(6)  # Page load hone do

        # Poora text nikalo
        body = driver.find_element(By.TAG_NAME, "body")
        text = body.text.strip()

        title = driver.title

        return {
            "url": url,
            "title": title,
            "text": text,
            "scraped_at": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"Error {url}: {e}")
        return None

def run_scraper():
    print("Scraping is about to begin...")
    driver = get_driver()
    results = []

    for url in PAGES:
        data = scrape_page(driver, url)
        if data and len(data["text"]) > 100:
            results.append(data)
            print(f"✅ Got {len(data['text'])} chars from {url}")
        else:
            print(f"❌ Failed: {url}")
        time.sleep(2)

    driver.quit()

    with open("data/raw/netsol_raw.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nDone! {len(results)} pages scraped!")
    return results

if __name__ == "__main__":
    run_scraper()