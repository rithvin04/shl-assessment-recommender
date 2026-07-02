import requests
import os

URL = "https://tcp-us-prod-rnd.shl.com/voiceRater/shl-ai-hiring/shl_product_catalog.json"

os.makedirs("data", exist_ok=True)

response = requests.get(URL)

print("Status:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))

with open("data/shl_catalog_raw.json", "wb") as f:
    f.write(response.content)

print("Saved raw file")
print("File size:", len(response.content), "bytes")