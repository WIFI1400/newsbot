from telegram import Bot
from telegram.error import TelegramError
import logging
from config import BOT_TOKEN, CHANNEL_ID
import random

class TelegramService:
    def __init__(self):
        self.bot = Bot(token=BOT_TOKEN)
        self.hashtags = [
            'Технологии', 'IT', 'Наука', 'Инновации', 'Программирование',
            'AI', 'Кибербезопасность', 'Разработка', 'Техника', 'ITновости'
        ]
    
    def format_message(self, title, summary, link):
        """Форматирование сообщения для Telegram"""
        # Выбираем случайные хештеги
        selected_hashtags = random.sample(self.hashtags, 3)
        
        message = f"🚀 *{title}*\n\n"
        message += f"{summary}\n\n"
        message += f"🔗 [Читать подробнее]({link})\n\n"
        message += " ".join(f"#{tag}" for tag in selected_hashtags)
        
        return message
    
    async def send_post(self, title, summary, link, image_data=None):
        """Отправка поста в канал"""
        try:
            message = self.format_message(title, summary, link)
            
            if image_data:
                # Отправляем с изображением
                await self.bot.send_photo(
                    chat_id=CHANNEL_ID,
                    photo=image_data,
                    caption=message,
                    parse_mode='Markdown'
                )
            else:
                # Отправляем без изображения
                await self.bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=message,
                    parse_mode='Markdown',
                    disable_web_page_preview=False
                )
            
            logging.info("✅ Post sent successfully")
            return True
            
        except TelegramError as e:
            logging.error(f"Telegram error: {e}")
            return False
        except Exception as e:
            logging.error(f"Error sending post: {e}")
            return False
