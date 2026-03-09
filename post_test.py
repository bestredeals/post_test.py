import requests

BOT_TOKEN = "8557388882:AAEj4puUuzPe_IaYQatP_B1h4P610q5j2Lg"
CHAT_ID = "@bestredeals"

message = "✅ Automation is working"

requests.post(
    f"https://api.telegram.org/bot{8557388882:AAEj4puUuzPe_IaYQatP_B1h4P610q5j2Lg}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)
