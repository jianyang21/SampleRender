from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import time
import json
import os

# === Firebase Initialization ===
cred_dict = json.loads(os.environ["FIREBASE_CREDENTIALS_JSON"])
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)

db = firestore.client()
collection_ref = db.collection("tops_Medium_Size")

# === Main Scraper Function ===
def scrape_divided_dresses():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    
    driver = webdriver.Chrome(options=chrome_options)

    base_url = "https://www2.hm.com/en_in/women/shop-by-product/dresses.html?sizes=womenswear%3BNO_FORMAT%5BSML%5D%3BM&page="
    pages = range(1, 20)

    for page in pages:
        url = base_url + str(page)
        driver.get(url)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Scraping Page {page}: {url}")
        time.sleep(5)

        titles = driver.find_elements(By.CSS_SELECTOR, 'h2.da7fd3.fcf345.c2f341.bfa3ef')
        prices = driver.find_elements(By.CSS_SELECTOR, 'span.c2de6d.f1c5a4')

        for i in range(min(len(titles), len(prices))):
            name = titles[i].text.strip()
            price = prices[i].text.strip()
            doc_id = f"{name}-{price}".replace(" ", "_")

            doc = collection_ref.document(doc_id).get()
            if not doc.exists:
                collection_ref.document(doc_id).set({
                    "name": name,
                    "price": price,
                    "page": page,
                    "category": "Divided Dresses",
                    "size_tag": "Small",
                    "timestamp": datetime.now().isoformat()
                })
                print(f"  ➕ New item added: {name} | {price}")
            else:
                print(f" Already exists: {name} | {price}")

    driver.quit()

# === Run every 30 minutes ===
while True:
    scrape_divided_dresses()
    print("\n⏳ Waiting 30 minutes before next check...\n")
    time.sleep(1800)
