import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = "@bestredeals"

message = "✅ Automation is working"

response = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    },
    timeout=30
)

print(response.status_code)
print(response.text)
response.raise_for_status()
