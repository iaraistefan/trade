from flask import Flask, request
import requests

app = Flask(__name__)

# Configurare bot Telegram
TOKEN = "8164160967:AAGt8kUeFe1--8al4Nw8LbsiXLzBCWhjHrE"
CHAT_ID = "-1002671409467"
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    message = data.get("text", "⚠️ Nu am primit niciun mesaj.")
    
    # Trimitem mesajul către Telegram
    requests.post(TELEGRAM_URL, json={"chat_id": CHAT_ID, "text": message})
    
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
