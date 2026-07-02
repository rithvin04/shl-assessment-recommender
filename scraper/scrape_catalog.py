import requests
from bs4 import BeautifulSoup

URL = "https://www.shl.com/products/product-catalog/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)

print("Status:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

print("Page Title:", soup.title.text)

tables = soup.find_all("table")

print("Number of tables:", len(tables))