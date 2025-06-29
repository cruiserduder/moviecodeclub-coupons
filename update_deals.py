import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

headers = {
    "User-Agent": "Mozilla/5.0"
}

all_deals = {
    "4K UHD": [],
    "HD": []
}

# ---------- 4K UHD Scraping (Multi-Page) ----------
format_label = "4K UHD"
base_url = "https://moviecodeclub.com/collections/4k-codes"
page = 1

while True:
    paged_url = f"{base_url}?page={page}"
    print(f"Scraping {format_label} page {page}...")
    response = requests.get(paged_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.select("li.grid__item")
    if not products:
        break

    for product in products:
        title_tag = product.select_one(".card__heading")
        price_tag = product.select_one(".price-item--sale") or product.select_one(".price-item--regular")
        compare_tag = product.select_one(".price-item--regular")
        if not title_tag or not price_tag:
            continue

        title = title_tag.text.strip()
        current_price = re.search(r"\$[\d\.]+", price_tag.text)
        current_price = current_price.group(0) if current_price else "$0.00"

        original_price = ""
        if compare_tag:
            compare = re.search(r"\$[\d\.]+", compare_tag.text)
            if compare and compare.group(0) != current_price:
                original_price = compare.group(0)

        # Discount %
        try:
            if original_price:
                cur = float(current_price.replace("$", ""))
                orig = float(original_price.replace("$", ""))
                discount = f"{round((1 - cur / orig) * 100)}% off" if cur < orig else ""
            else:
                discount = ""
        except:
            discount = ""

        link_tag = product.find("a", href=True)
        link = "https://moviecodeclub.com" + link_tag["href"] if link_tag else base_url

        all_deals[format_label].append({
            "title": title,
            "price": current_price,
            "original_price": original_price,
            "discount": discount,
            "link": link,
            "format": format_label,
            "added": datetime.utcnow().strftime("%Y-%m-%d")
        })

    page += 1

# Reverse to get newest → oldest
all_deals["4K UHD"].reverse()

# ---------- HD Scraping (Page 1 Only) ----------
format_label = "HD"
url = "https://moviecodeclub.com/collections/hd-codes-1"
print(f"Scraping {format_label} page 1 only...")
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

products = soup.select("li.grid__item")
for product in products:
    title_tag = product.select_one(".card__heading")
    price_tag = product.select_one(".price-item--sale") or product.select_one(".price-item--regular")
    compare_tag = product.select_one(".price-item--regular")
    if not title_tag or not price_tag:
        continue

    title = title_tag.text.strip()
    current_price = re.search(r"\$[\d\.]+", price_tag.text)
    current_price = current_price.group(0) if current_price else "$0.00"

    original_price = ""
    if compare_tag:
        compare = re.search(r"\$[\d\.]+", compare_tag.text)
        if compare and compare.group(0) != current_price:
            original_price = compare.group(0)

    try:
        if original_price:
            cur = float(current_price.replace("$", ""))
            orig = float(original_price.replace("$", ""))
            discount = f"{round((1 - cur / orig) * 100)}% off" if cur < orig else ""
        else:
            discount = ""
    except:
        discount = ""

    link_tag = product.find("a", href=True)
    link = "https://moviecodeclub.com" + link_tag["href"] if link_tag else url

    all_deals[format_label].append({
        "title": title,
        "price": current_price,
        "original_price": original_price,
        "discount": discount,
        "link": link,
        "format": format_label,
        "added": datetime.utcnow().strftime("%Y-%m-%d")
    })

# Reverse HD too for newest first
all_deals["HD"].reverse()

# ---------- Write files ----------
with open("deals_4k.json", "w") as f:
    json.dump(all_deals["4K UHD"], f, indent=2)

with open("deals_hd.json", "w") as f:
    json.dump(all_deals["HD"], f, indent=2)

print(f"✅ Saved {len(all_deals['4K UHD'])} 4K deals → deals_4k.json")
print(f"✅ Saved {len(all_deals['HD'])} HD deals → deals_hd.json")