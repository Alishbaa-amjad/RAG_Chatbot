import json
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://netsoltech.com"

def get_all_urls():
    print("Step 1 — Collecting URLs from sitemap...")
    skip_langs = ['/en-us', '/en-gb', '/de', '/es', '/id', '/th', '/fr', '/ar']
    urls = set()

    # Sitemap se URLs nikalo
    try:
        response = requests.get(
            f"{BASE_URL}/sitemap.xml",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        soup = BeautifulSoup(response.text, 'xml')
        locs = soup.find_all('loc')
        for loc in locs:
            url = loc.text.strip()
            if not any(lang in url for lang in skip_langs):
                urls.add(url)
        print(f"Found {len(urls)} URLs from sitemap")
    except Exception as e:
        print(f"Sitemap error: {e}")

    # Extra pages from blogs/case-studies/whitepapers
    print("Step 2 — Finding extra URLs from blogs/case-studies/whitepapers...")
    extra_pages = [
        "/insights/blogs",
        "/insights/case-studies",
        "/insights/whitepapers",
        "/insights/testimonials",
        "/about-us/management-team",
        "/about-us/board-of-directors",
        "/services",
        "/products",
        "/solutions",
    ]

    for page in extra_pages:
        try:
            r = requests.get(
                BASE_URL + page,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10
            )
            soup = BeautifulSoup(r.text, 'html.parser')
            links = soup.find_all('a', href=True)
            for a in links:
                href = a['href']
                if href.startswith('/') and not any(lang in href for lang in skip_langs):
                    full = BASE_URL + href.split('?')[0].split('#')[0]
                    if BASE_URL in full:
                        urls.add(full)
                elif BASE_URL in href and not any(lang in href for lang in skip_langs):
                    urls.add(href.split('?')[0].split('#')[0])
            print(f"  Found {len(urls)} total so far from {page}")
            time.sleep(1)
        except Exception as e:
            print(f"  Error on {page}: {e}")

    # Filter karo — sirf netsoltech.com URLs
    final_urls = [
        u for u in urls
        if BASE_URL in u
        and not any(lang in u for lang in skip_langs)
        and u.strip() != BASE_URL + '/'
        or u == BASE_URL + '/'
    ]

    print(f"\nTotal unique URLs found: {len(final_urls)}")
    return final_urls


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--page-load-strategy=none")
    options.add_argument("user-agent=Mozilla/5.0")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.set_page_load_timeout(180)
    return driver


def scrape_page(driver, url):
    for attempt in range(3):
        try:
            driver.get(url)
            try:
                WebDriverWait(driver, 30).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
            except:
                pass

            time.sleep(8)

            try:
                driver.execute_script("""
                    var elements = document.querySelectorAll(
                        'nav, footer, header, script, style, .cookie-banner, #cookie-notice'
                    );
                    elements.forEach(e => e.remove());
                """)
            except:
                pass

            body = driver.find_element(By.TAG_NAME, "body")
            text = body.text.strip()
            title = driver.title

            if len(text) < 80:
                return None

            return {
                "url": url,
                "title": title,
                "text": text,
                "scraped_at": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"⚠️ Attempt {attempt+1} failed: {type(e).__name__} — retrying...")
            time.sleep(10)

    print(f"❌ All 3 attempts failed: {url}")
    return None


def run_scraper():
    # Step 1 — URLs collect karo automatically
    all_urls = get_all_urls()

    print(f"\nStarting scraper — Total URLs to scrape: {len(all_urls)}")
    driver = get_driver()
    results = []

    for i, url in enumerate(all_urls):
        print(f"[{i+1}/{len(all_urls)}] Scraping: {url}")

        try:
            data = scrape_page(driver, url)
        except Exception:
            print("Driver crashed — restarting...")
            try:
                driver.quit()
            except:
                pass
            driver = get_driver()
            data = scrape_page(driver, url)

        if data:
            results.append(data)
            print(f"✅ Got {len(data['text'])} chars")
        else:
            print(f"❌ Skipped")

        time.sleep(2)

        if (i + 1) % 10 == 0:
            with open("data/raw/netsol_raw.json", "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"--- Saved {len(results)} pages so far ---")

    driver.quit()
    with open("data/raw/netsol_raw.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nDone! Total {len(results)} pages scraped!")


if __name__ == "__main__":
    run_scraper()