
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# === Config: Token și Chat ID ===
BOT_TOKEN = "8164160967:AAGt8kUeFe1--8al4Nw8LbsiXLzBCWhjHrE"
CHAT_ID = "-1002671409467"  # Canal: stefitradesignal

# === Funcție trimis mesaj Telegram ===
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"  # sau "Markdown" dacă preferi
    }
    response = requests.post(url, json=payload)
    print(f"[Telegram] Trimis: {payload}")
    print(f"[Telegram] Status: {response.status_code} | Răspuns: {response.text}")

# === Webhook TradingView ===
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Acceptă text simplu sau JSON cu 'message'
        message = request.get_data(as_text=True).strip()
        print(f"[Webhook] Mesaj primit:\n{message}")

        if not message:
            raise ValueError("Mesajul primit este gol.")

        send_telegram_message(message)
        return jsonify({"status": "ok", "delivered": True}), 200
    except Exception as e:
        print(f"[EROARE Webhook] {e}")
        return jsonify({"status": "error", "details": str(e)}), 400

# === Test GET ===
@app.route("/", methods=["GET"])
def index():
    return "✅ Webhook funcționează și așteaptă alerte!"

if __name__ == "__main__":
    app.run(port=5000)
