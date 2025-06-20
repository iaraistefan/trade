import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Tokenul și Chat ID-ul din variabile de mediu
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Funcția care trimite mesajul în Telegram
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"  # Poți schimba cu None dacă nu vrei formatări
    }
    response = requests.post(url, json=payload)
    print(f"[Telegram] Trimitem: {payload}")
    print(f"[Telegram] Status: {response.status_code} | Răspuns: {response.text}")

# Webhook-ul care primește alertă simplă (fără JSON)
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        message = request.get_data(as_text=True).strip()
        print(f"[Webhook] Mesaj primit:\n{message}")

        if not message:
            raise ValueError("Mesajul primit este gol.")

        send_telegram_message(message)
        return jsonify({"status": "ok", "delivered": True}), 200
    except Exception as e:
        print(f"[EROARE Webhook] {e}")
        return jsonify({"status": "error", "details": str(e)}), 400

# Endpoint GET de test
@app.route("/", methods=["GET"])
def index():
    return "✅ Webhook este activ!"
