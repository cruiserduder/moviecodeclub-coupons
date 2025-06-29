import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# URLs to scrape
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

    # Product cards vary across Shopify themes, may need adjusting
    products = soup.select(".product-card, .grid__item")

    for product in products:
        title_tag = product.select_one(".product-card__title, .full-unstyled-link")
        price_tag = product.select_one(".price-item--sale, .price-item--regular")
        compare_tag = product.select_one(".price-item--regular")

        if compare_tag:
    raw_compare = compare_tag.text.strip().replace("\u00a0", " ")
    if raw_compare != current_price:
        original_price = raw_compare
    else:
        original_price = ""
else:
    original_price = ""

        try:
            cur = float(current_price.replace("$", ""))
            orig = float(original_price.replace("$", ""))
            discount_pct = f"{round((1 - cur / orig) * 100)}% off" if cur < orig else ""
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

# Save to deals.json
with open("deals.json", "w") as f:
    json.dump(all_deals, f, indent=2)

print(f"✅ {len(all_deals)} deals saved to deals.json")
