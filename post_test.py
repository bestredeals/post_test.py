import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = "@bestredeals"
AFFILIATE_TAG = "sherifaly-20"

AMAZON_DEALS_URL = "https://www.amazon.com/gp/goldbox"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def send_message(text):
    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text
        },
        timeout=30
    )
    print(response.status_code, response.text)
    response.raise_for_status()

def make_affiliate_link(url):
    separator = "&" if "?" in url else "?"
    return f"{url}{separator}tag={AFFILIATE_TAG}"

def normalize_product_url(href):
    full_url = urljoin("https://www.amazon.com", href)

    # Keep only real product URLs with ASINs
    match = re.search(r"/dp/([A-Z0-9]{10})", full_url)
    if match:
        asin = match.group(1)
        return f"https://www.amazon.com/dp/{asin}"

    match = re.search(r"/gp/product/([A-Z0-9]{10})", full_url)
    if match:
        asin = match.group(1)
        return f"https://www.amazon.com/dp/{asin}"

    return None

response = requests.get(AMAZON_DEALS_URL, headers=HEADERS, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
links = soup.find_all("a", href=True)

posted = 0
seen = set()

BAD_TEXT = {
    "all", "cart", "returns", "registry", "prime", "customer service",
    "gift cards", "sell", "today's deals"
}

for a in links:
    href = a["href"]
    title = a.get_text(" ", strip=True)

    if not title:
        continue

    if title.lower() in BAD_TEXT:
        continue

    product_url = normalize_product_url(href)
    if not product_url:
        continue

    if product_url in seen:
        continue
    seen.add(product_url)

    affiliate_link = make_affiliate_link(product_url)

    message = f"""🔥 DEAL ALERT

{title}

Grab it here:
{affiliate_link}
"""

    send_message(message)
    posted += 1

    if posted >= 3:
        break

if posted == 0:
    send_message("No product deals found right now.")
