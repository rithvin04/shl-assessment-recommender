import requests
from bs4 import BeautifulSoup

url = "https://www.shl.com/solutions/products/product-catalog/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)

with open("catalog.html", "w", encoding="utf-8") as f:
    f.write(response.text)

print("HTML saved as catalog.html")

soup = BeautifulSoup(response.text, "html.parser")

print("Title:", soup.title.text if soup.title else "No title")