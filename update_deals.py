import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

# Collection URLs
collection_urls = {
    "4K UHD": "https://moviecodeclub.com/collections/4k-codes",
    "HD": "https://moviecodeclub.com/collections/hd-codes"
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

all_deals = []

# Loop through each collection
for format_label, base_url in collection_urls.items():
    page = 1
    while True:
        paged_url = f"{base_url}?page={page}"
        print(f"Scraping {format_label} page {page}...")

        response = requests.get(paged_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        products = soup.select("li.grid__item")
        if not products:
            print(f"No more products on page {page} — stopping.")
            break

        for product in products:
            title_tag = product.select_one(".card__heading")
            price_tag = product.select_one(".price-item--sale") or product.select_one(".price-item--regular")
            compare_tag = product.select_one(".price-item--regular")

            if not title_tag or not price_tag:
                continue

            # Clean title
            title = title_tag.text.strip()

            # Extract current price
            current_price_match = re.search(r"\$[\d\.]+", price_tag.text)
            current_price = current_price_match.group(0) if current_price_match else "$0.00"

            # Extract original price (if different)
            if compare_tag:
                compare_match = re.search(r"\$[\d\.]+", compare_tag.text)
                if compare_match and compare_match.group(0) != current_price:
                    original_price = compare_match.group(0)
                else:
                    original_price = ""
            else:
                original_price = ""

            # Discount calculation
            try:
                if original_price:
                    cur = float(current_price.replace("$", ""))
                    orig = float(original_price.replace("$", ""))
                    discount_pct = f"{round((1 - cur / orig) * 100)}% off" if cur < orig else ""
                else:
                    discount_pct = ""
            except:
                discount_pct = ""

            # Product link
            link_tag = product.find("a", href=True)
            product_link = "https://moviecodeclub.com" + link_tag["href"] if link_tag else base_url

            # Add to list
            deal = {
                "title": title,
                "price": current_price,
                "original_price": original_price,
                "discount": discount_pct,
                "link": product_link,
                "format": format_label,
                "added": datetime.utcnow().strftime("%Y-%m-%d")
            }

            all_deals.append(deal)

        page += 1  # Go to next page

# Save to JSON
with open("deals.json", "w") as f:
    json.dump(all_deals, f, indent=2)

print(f"✅ {len(all_deals)} total deals saved to deals.json")