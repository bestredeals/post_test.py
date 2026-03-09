import os
import requests
import xml.etree.ElementTree as ET

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = "@bestredeals"
AFFILIATE_TAG = "bestredeals-20"  # replace if needed

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

def make_affiliate_link(url):
    if "amazon.com" in url:
        separator = "&" if "?" in url else "?"
        return f"{url}{separator}tag={AFFILIATE_TAG}"
    return url

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

    affiliate_link = make_affiliate_link(link)

    message = f"""🔥 DEAL ALERT

{title}

Grab it here:
{affiliate_link}
"""

    send_message(message)
    posted += 1

    if posted >= 3:
        break
