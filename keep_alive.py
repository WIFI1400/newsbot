from flask import Flask
import threading
import requests
import time
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 News Bot is alive!"

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

def ping_self():
    """Пингует себя для предотвращения сна"""
    try:
        if os.getenv('RENDER_URL'):
            requests.get(os.getenv('RENDER_URL'), timeout=10)
            print("🔄 Self-ping executed")
    except Exception as e:
        print(f"❌ Self-ping failed: {e}")

def start_ping_loop():
    """Запускает периодический пинг"""
    def ping_loop():
        while True:
            time.sleep(300)  # Пинг каждые 5 минут
            ping_self()
    
    ping_thread = threading.Thread(target=ping_loop)
    ping_thread.daemon = True
    ping_thread.start()
    print("✅ Ping loop started")
