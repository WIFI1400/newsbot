from flask import Flask
import threading
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Telegram News Bot is running!"

@app.route('/health')
def health():
    return {"status": "ok", "service": "telegram-news-bot"}

def run_flask():
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def start_keep_alive():
    """Запускает Flask сервер в отдельном потоке"""
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    print("✅ Keep-alive server started")

# Автоматически запускаем при импорте
start_keep_alive()
