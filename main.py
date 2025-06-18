import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Tokenul și Chat ID-ul le poți seta ca variabile de mediu în Render
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Funcție care trimite mesajul către Telegram
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": None  # ← poți pune "HTML" sau "MarkdownV2" dacă vrei formatare
    }
    response = requests.post(url, json=payload)
    print(f"[Telegram] Status: {response.status_code} | Răspuns: {response.text}")

# Ruta webhook unde TradingView trimite date
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)  # ← forțăm Flask să încerce și dacă nu e "application/json"
        print(f"[Webhook] Mesaj primit: {data}")
        message = data.get("message", "⚠️ Nu a fost găsit câmpul 'message'")
        send_telegram_message(message)
        return jsonify({"status": "ok", "delivered": True}), 200
    except Exception as e:
        print(f"[EROARE Webhook] {e}")
        return jsonify({"status": "error", "details": str(e)}), 400

# Endpoint de test GET — opțional
@app.route("/", methods=["GET"])
def index():
    return "✅ Webhook este activ!"
