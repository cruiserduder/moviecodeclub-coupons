
import json
from datetime import datetime

# Simulated "fresh" data – replace this with web scraping logic later
updated_coupons = [
    {"code": "WELCOME10", "deal": "10% off first order", "notes": "Still valid for new users"},
    {"code": "MOVIEJULY5", "deal": "$5 off $30+", "notes": "July 2025 update"},
    {"code": "SUMMERSTACK", "deal": "Stack 2+ codes for 20% off", "notes": "New summer stack combo"},
    {"code": "FLASHDEAL", "deal": "15% off today only", "notes": "Auto-updated daily"},
    {"code": "VIPMOVIE25", "deal": "25% off VIP members", "notes": "Requires login"}
]

# Save to coupons.json
with open("coupons.json", "w") as f:
    json.dump(updated_coupons, f, indent=2)

print(f"Updated coupons.json with {len(updated_coupons)} entries on {datetime.now().isoformat()}")
