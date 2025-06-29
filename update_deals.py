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

for format_label, url in collection_urls.items():
    print(f"Scraping {format_label} deals...")

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.select(".product-card, .grid__item")

    for product in products:
        title_tag = product.select_one(".product-card__title, .full-unstyled-link")
        price_tag = product.select_one(".price-item--sale, .price-item--regular")
        compare_tag = product.select_one(".price-item--regular")

        if not title_tag or not price_tag:
            continue

        title = title_tag.text.strip()

        # Extract current price (regex to remove junk like "Sale price")
        current_price_match = re.search(r"\$[\d\.]+", price_tag.text)
        current_price = current_price_match.group(0) if current_price_match else "$0.00"

        # Extract original price only if different and available
        if compare_tag:
            compare_text = compare_tag.text.strip()
            compare_match = re.search(r"\$[\d\.]+", compare_text)
            if compare_match and compare_match.group(0) != current_price:
                original_price = compare_match.group(0)
            else:
                original_price = ""
        else:
            original_price = ""

        # Calculate discount
        try:
            if original_price:
                cur = float(current_price.replace("$", ""))
                orig = float(original_price.replace("$", ""))
                discount_pct = f"{round((1 - cur / orig) * 100)}% off" if cur < orig else ""
            else:
                discount_pct = ""
        except:
            discount_pct = ""

        link_tag = product.find("a", href=True)
        product_link = "https://moviecodeclub.com" + link_tag["href"] if link_tag else url

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

# Save to JSON
with open("deals.json", "w") as f:
    json.dump(all_deals, f, indent=2)

print(f"✅ {len(all_deals)} deals saved to deals.json")
