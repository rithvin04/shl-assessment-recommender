from playwright.sync_api import sync_playwright

URL = "https://www.shl.com/solutions/products/product-catalog/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page(viewport={"width": 1920, "height": 1080})

    page.goto(URL, timeout=120000)

    page.wait_for_load_state("networkidle")

    print("Current URL:", page.url)
    print("Title:", page.title())

    page.screenshot(path="catalog.png", full_page=True)

    browser.close()