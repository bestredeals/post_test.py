import os
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, parse_qs

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = "@bestredeals"
AFFILIATE_TAG = "sherifaly-20"

RSS_URL = "https://slickdeals.net/newsearch.php?mode=frontpage&searcharea=deals&rss=1"

def send_message(text):
    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text
        },
        timeout=30
    )
    response.raise_for_status()

def extract_amazon_url(url):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    # Some deal links may contain a real target URL in query params
    for key in ["url", "u", "redirect", "redirectUrl"]:
        if key in query and query[key]:
            candidate = query[key][0]
            if "amazon.com" in candidate:
                return candidate

    if "amazon.com" in url:
        return url

    return None

def make_affiliate_link(url):
    separator = "&" if "?" in url else "?"
    return f"{url}{separator}tag={AFFILIATE_TAG}"

rss = requests.get(RSS_URL, timeout=30)
rss.raise_for_status()

root = ET.fromstring(rss.content)
items = root.findall(".//item")

posted = 0

for item in items:
    title = item.findtext("title", default="Deal")
    link = item.findtext("link", default="")

    if "amazon" not in title.lower() and "amazon" not in link.lower():
        continue

    amazon_url = extract_amazon_url(link)
    if not amazon_url:
        continue

    affiliate_link = make_affiliate_link(amazon_url)

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
    send_message("No Amazon deals found right now.")
