# app.py
from flask import Flask, request, jsonify
import requests
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        alert_msg = data.get('message', '⚠️ Alertă fără mesaj')
        
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={
                "chat_id": CHAT_ID,
                "text": alert_msg,
                "parse_mode": "HTML"
            }
        )
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        logging.error(f"Eroare: {str(e)}")
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
