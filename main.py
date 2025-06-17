import os
from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = os.getenv("8164160967:AAGt8kUeFe1--8al4Nw8LbsiXLzBCWhjHrE")
CHAT_ID = os.getenv("-1002671409467")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    message = data.get("message", "No message received.")
    send_telegram_message(message)
    return {"status": "ok"}

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=payload)

