import asyncio
import logging
import time
from datetime import datetime
from news_service import NewsService
from gemini_service import GeminiService
from image_service import ImageService
from telegram_service import TelegramService
from keep_alive import start_keep_alive, start_ping_loop
from config import POST_INTERVAL

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)

class NewsBot:
    def __init__(self):
        self.news_service = NewsService()
        self.gemini_service = GeminiService()
        self.image_service = ImageService()
        self.telegram_service = TelegramService()
        self.is_running = True
    
    async def initialize(self):
        """Инициализация сервисов"""
        await self.news_service.init_session()
        logging.info("✅ All services initialized")
    
    async def create_news_post(self, news_item):
        """Создание поста с контентом"""
        try:
            # Генерируем описание через Gemini
            summary = await self.gemini_service.generate_summary(
                news_item['title'], 
                news_item['description']
            )
            
            if not summary:
                # Fallback описание
                summary = news_item['description'][:200] + "..." if news_item['description'] else "Интересная IT-новость. Читайте подробнее по ссылке."
            
            # Генерируем изображение
            image_data = await self.image_service.generate_tech_image(news_item['title'])
            
            return {
                'title': news_item['title'],
                'summary': summary,
                'link': news_item['link'],
                'image_data': image_data
            }
            
        except Exception as e:
            logging.error(f"Error creating post: {e}")
            return None
    
    async def post_news_cycle(self):
        """Один цикл публикации новости"""
        try:
            logging.info("🔄 Starting news cycle...")
            
            # Получаем новости
            all_news = await self.news_service.fetch_news()
            logging.info(f"📰 Found {len(all_news)} news items")
            
            if not all_news:
                logging.warning("❌ No news found")
                return False
            
            # Получаем свежие новости
            fresh_news = self.news_service.get_fresh_news(all_news)
            logging.info(f"🆕 Fresh news: {len(fresh_news)} items")
            
            if not fresh_news:
                logging.info("ℹ️ No fresh news to post")
                return False
            
            # Выбираем случайную новость
            selected_news = fresh_news[0]  # Берем самую свежую
            logging.info(f"📝 Selected: {selected_news['title'][:50]}...")
            
            # Создаем контент для поста
            post_data = await self.create_news_post(selected_news)
            
            if post_data:
                # Публикуем в Telegram
                success = await self.telegram_service.send_post(
                    title=post_data['title'],
                    summary=post_data['summary'],
                    link=post_data['link'],
                    image_data=post_data['image_data']
                )
                
                if success:
                    self.news_service.mark_as_posted(selected_news['link'])
                    logging.info("✅ News posted successfully!")
                    return True
                else:
                    logging.error("❌ Failed to post news")
                    return False
            else:
                logging.error("❌ Failed to create post content")
                return False
                
        except Exception as e:
            logging.error(f"❌ News cycle error: {e}")
            return False
    
    async def run(self):
        """Основной цикл бота"""
        await self.initialize()
        
        # Запускаем keep-alive
        start_keep_alive()
        start_ping_loop()
        
        logging.info("🤖 News Bot started successfully!")
        logging.info(f"⏰ Post interval: {POST_INTERVAL} seconds")
        
        cycle_count = 0
        
        while self.is_running:
            try:
                cycle_count += 1
                logging.info(f"🔄 Cycle #{cycle_count}")
                
                success = await self.post_news_cycle()
                
                if success:
                    next_post = datetime.now().timestamp() + POST_INTERVAL
                    logging.info(f"✅ Cycle completed. Next post at: {datetime.fromtimestamp(next_post).strftime('%H:%M %d.%m.%Y')}")
                else:
                    logging.warning("⚠️ Cycle completed with issues")
                
                # Ждем перед следующим циклом
                logging.info(f"💤 Waiting {POST_INTERVAL} seconds...")
                await asyncio.sleep(POST_INTERVAL)
                
            except Exception as e:
                logging.error(f"💥 Critical error in main loop: {e}")
                logging.info("🔄 Restarting in 60 seconds...")
                await asyncio.sleep(60)
    
    async def stop(self):
        """Остановка бота"""
        self.is_running = False
        await self.news_service.close()
        logging.info("🛑 Bot stopped")

async def main():
    bot = NewsBot()
    
    try:
        await bot.run()
    except KeyboardInterrupt:
        logging.info("🛑 Received stop signal")
        await bot.stop()
    except Exception as e:
        logging.error(f"💥 Fatal error: {e}")
        await bot.stop()

if __name__ == "__main__":
    # Запуск бота
    asyncio.run(main())
