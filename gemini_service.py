import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_CONFIG
import logging

# Настройка Gemini
genai.configure(api_key=GEMINI_API_KEY)

class GeminiService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def generate_summary(self, title, description):
        """Генерация краткого описания новости"""
        try:
            prompt = f"""
            Создай краткое и интересное описание для IT-новости на основе заголовка и текста.
            Описание должно быть 100-150 слов, информативным и engaging.
            
            Заголовок: {title}
            Текст: {description[:1000] if description else "Нет подробного текста"}
            
            Требования:
            - Только текст, без форматирования
            - На русском языке
            - Фактический и информативный стиль
            - Без упоминания что это AI-генерация
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logging.error(f"Gemini summary error: {e}")
            return None
    
    async def generate_image_prompt(self, title):
        """Генерация промпта для изображения"""
        try:
            prompt = f"""
            Создай короткий промпт на английском для генерации изображения на тему: "{title}"
            
            Требования:
            - 10-15 слов
            - Только промпт, без объяснений
            - Абстрактная технологическая тематика
            - Без текста на изображении
            Пример: "futuristic technology abstract background with glowing elements"
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logging.error(f"Gemini image prompt error: {e}")
            return f"technology innovation {title}"
