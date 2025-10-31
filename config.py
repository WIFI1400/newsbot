import os

# Настройки бота
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
RENDER_URL = os.getenv('RENDER_URL')

# Интервал между постами (4 часа)
POST_INTERVAL = 4 * 60 * 60  # 4 часа в секундах

# Источники новостей
NEWS_SOURCES = [
    "https://habr.com/ru/rss/hub/security/all/?fl=ru",
    "https://habr.com/ru/rss/hub/python/all/?fl=ru",
    "https://habr.com/ru/rss/hub/ai/all/?fl=ru",
    "https://www.securitylab.ru/_services/export/rss/",
    "https://vc.ru/feed",
    "https://3dnews.ru/news/rss",
]

# Запрещенные ключевые слова
FORBIDDEN_KEYWORDS = [
    'войн', 'смиш', 'войска', 'спецоперац', 'убийств', 
    'теракт', 'catwar', 'политик', 'криминал', 'дтп'
]

# Настройки Gemini
GEMINI_CONFIG = {
    'temperature': 0.7,
    'top_p': 0.8,
    'top_k': 40,
    'max_output_tokens': 500,
}
