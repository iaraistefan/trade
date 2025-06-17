import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Preluăm variabilele din Environment (le setezi în Render dashboard)
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Funcția care trimite mesajul în Telegram
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "MarkdownV2"  # sau "HTML" dacă preferi alt format
    }
    requests.post(url, json=payload)

# Punctul de intrare pentru webhook-ul TradingView
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    message = data.get("message", "⚠️ Mesaj inexistent sau gol")
    send_telegram_message(message)
    return jsonify({"status": "ok"}), 200
