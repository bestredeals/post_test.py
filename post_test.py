import os
import requests
import xml.etree.ElementTree as ET

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = "@bestredeals"

RSS_URL = "https://slickdeals.net/newsearch.php?mode=frontpage&searcharea=deals&rss=1"

def send_message(text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

rss = requests.get(RSS_URL)
root = ET.fromstring(rss.content)

items = root.findall(".//item")

for item in items[:3]:

    title = item.find("title").text
    link = item.find("link").text

    message = f"""
🔥 DEAL ALERT

{title}

See deal:
{link}
"""

    send_message(message)
