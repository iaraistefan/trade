import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Variabile de mediu pentru token și chat ID (din Render dashboard)
BOT_TOKEN = os.getenv("8164160967:AAGt8kUeFe1--8al4Nw8LbsiXLzBCWhjHrE")
CHAT_ID = os.getenv("-1002671409467")

# Funcție pentru a trimite mesajul în Telegram
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"  # alternativ: None sau "MarkdownV2"
    }
    response = requests.post(url, json=payload)
    print(f"[Telegram API] Status: {response.status_code} | Response: {response.text}")

# Webhook-ul care primește datele de la TradingView
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        print(f"[Webhook] Received data: {data}")
        message = data.get("message", "⚠️ Nu a fost găsit niciun câmp 'message'")
        send_telegram_message(message)
        return jsonify({"status": "ok", "message_sent": True}), 200
    except Exception as e:
        print(f"[Webhook Error] {e}")
        return jsonify({"status": "error", "details": str(e)}), 400

# Endpoint de test (GET) — opțional
@app.route("/", methods=["GET"])
def root():
    return "✅ Webhook Flask funcționează!"
