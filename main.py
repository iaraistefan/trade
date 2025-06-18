import os
import json
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Variabile de mediu pentru token și chat ID
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Funcție pentru trimiterea mesajului către Telegram
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    response = requests.post(url, json=payload)
    print(f"[Telegram] Status: {response.status_code} | Răspuns: {response.text}")

# Webhook care primește alerta din TradingView
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        raw_data = request.get_data().decode("utf-8")  # ← Extrage conținutul brut
        print(f"[Webhook] JSON primit: {raw_data}")

        parsed_data = json.loads(raw_data)  # ← Convertim JSON-ul brut într-un dicționar
        message = parsed_data.get("message", "⚠️ Nu a fost găsit câmpul 'message'")
        
        send_telegram_message(message)
        return jsonify({"status": "ok", "delivered": True}), 200
    except Exception as e:
        print(f"[EROARE Webhook] {e}")
        return jsonify({"status": "error", "details": str(e)}), 400

# Endpoint de test GET — opțional
@app.route("/", methods=["GET"])
def index():
    return "✅ Webhook activ și gata de trimitere în Telegram!"
