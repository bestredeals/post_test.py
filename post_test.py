import os
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

response = requests.get(AMAZON_DEALS_URL, headers=HEADERS, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

links = soup.find_all("a", href=True)

posted = 0
seen = set()

for a in links:
    href = a["href"]

    if "/dp/" not in href and "/gp/" not in href:
        continue

    full_url = urljoin("https://www.amazon.com", href)

    if full_url in seen:
        continue
    seen.add(full_url)

    title = a.get_text(strip=True)
    if not title:
        title = "Amazon Deal"

    affiliate_link = make_affiliate_link(full_url)

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
    send_message("No Amazon product links found on the deals page right now.")
