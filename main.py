from flask import Flask, request, jsonify
import requests
import os
import logging
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Configurație cu datele tale
TOKEN = "8164160967:AAGt8kUeFe1--8al4Nw8LbsiXLzBCWhjHrE"
CHAT_ID = "-1002671409467"
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Verifică datele primite
        data = request.json
        if not data:
            logging.error("Cerere fără date JSON")
            return jsonify({"status": "error", "message": "Date invalide"}), 400
            
        message = data.get('message', '⚠️ Mesaj gol')
        logging.info(f"Mesaj primit: {message[:100]}...")  # Loghează doar primele 100 de caractere

        # Trimite pe Telegram
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        
        response = requests.post(TELEGRAM_URL, json=payload, timeout=5)
        response.raise_for_status()  # Aruncă eroare pentru status 4XX/5XX
        
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        logging.error(f"Eroare: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, ssl_context='adhoc')
