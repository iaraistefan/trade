import os
import json
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Tokenul și Chat ID-ul din variabile de mediu
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Trimite mesajul către Telegram
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"  # poți pune None dacă nu vrei stilizare
    }
    response = requests.post(url, json=payload)
    print(f"[Telegram] Trimitem: {payload}")
    print(f"[Telegram] Status: {response.status_code} | Răspuns: {response.text}")

# Webhook-ul care primește alerta din TradingView
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        raw = request.get_data().decode("utf-8")
        print(f"[Webhook] JSON primit brut:\n{raw}")

        # Înlocuiește toate newline-urile brute cu \n escapate pentru JSON corect
        safe_json = raw.replace("\n", "\\n")
        data = json.loads(safe_json)

        message = data.get("message", "⚠️ Mesajul nu a fost găsit")
        send_telegram_message(message)
        return jsonify({"status": "ok", "delivered": True}), 200
    except Exception as e:
        print(f"[EROARE Webhook] {e}")
        return jsonify({"status": "error", "details": str(e)}), 400

# Endpoint GET de test
@app.route("/", methods=["GET"])
def index():
    return "✅ Webhook este activ!"
