import os
import json
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Tokenul botului și ID-ul chatului Telegram (setate ca variabile de mediu în Render)
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Trimite mesajul către Telegram
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"  # sau None dacă nu vrei formatare
    }
    response = requests.post(url, json=payload)
    print(f"[Telegram] Status: {response.status_code} | Răspuns: {response.text}")

# Webhook-ul care primește alertele din TradingView
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        raw_data = request.get_data().decode("utf-8")  # Extrage conținutul brut
        print(f"[Webhook] JSON primit: {raw_data}")

        # Transformă textul într-un dicționar Python
        parsed = json.loads(raw_data)
        message = parsed.get("message", "⚠️ Mesaj lipsă în payload-ul JSON")

        send_telegram_message(message)
        return jsonify({"status": "ok", "delivered": True}), 200
    except Exception as e:
        print(f"[EROARE Webhook] {e}")
        return jsonify({"status": "error", "details": str(e)}), 400

# Endpoint de test simplu
@app.route("/", methods=["GET"])
def index():
    return "✅ Webhook Flask funcționează corect!"
