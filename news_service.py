import feedparser
import aiohttp
import asyncio
import logging
from config import NEWS_SOURCES, FORBIDDEN_KEYWORDS
import random
from datetime import datetime, timedelta

class NewsService:
    def __init__(self):
        self.session = None
        self.posted_links = set()
    
    async def init_session(self):
        """Инициализация сессии"""
        if not self.session:
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(timeout=timeout)
    
    async def fetch_news(self):
        """Получение новостей из всех источников"""
        await self.init_session()
        
        all_news = []
        tasks = []
        
        for source in NEWS_SOURCES:
            task = self._fetch_source_news(source)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, list):
                all_news.extend(result)
        
        # Фильтруем и сортируем
        filtered_news = self._filter_news(all_news)
        return filtered_news
    
    async def _fetch_source_news(self, source):
        """Получение новостей из одного источника"""
        try:
            async with self.session.get(source) as response:
                if response.status == 200:
                    text = await response.text()
                    return self._parse_feed(text, source)
        except Exception as e:
            logging.error(f"Error fetching {source}: {e}")
        
        return []
    
    def _parse_feed(self, feed_text, source):
        """Парсинг RSS фида"""
        try:
            feed = feedparser.parse(feed_text)
            news_items = []
            
            for entry in feed.entries[:10]:  # Берем последние 10 новостей
                # Проверяем дату (только свежие новости)
                if hasattr(entry, 'published_parsed'):
                    news_date = datetime(*entry.published_parsed[:6])
                    if datetime.now() - news_date > timedelta(days=7):
                        continue
                
                title = getattr(entry, 'title', '').strip()
                link = getattr(entry, 'link', '').strip()
                description = getattr(entry, 'description', '').strip()
                
                if not title or not link:
                    continue
                
                # Фильтрация по ключевым словам
                if self._is_forbidden_content(title):
                    continue
                
                news_item = {
                    'title': title,
                    'link': link,
                    'description': description,
                    'source': source,
                    'published': getattr(entry, 'published', '')
                }
                
                news_items.append(news_item)
            
            return news_items
            
        except Exception as e:
            logging.error(f"Error parsing feed {source}: {e}")
            return []
    
    def _is_forbidden_content(self, title):
        """Проверка на запрещенный контент"""
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in FORBIDDEN_KEYWORDS)
    
    def _filter_news(self, news_items):
        """Фильтрация и сортировка новостей"""
        # Убираем дубликаты
        seen_links = set()
        unique_news = []
        
        for news in news_items:
            if news['link'] not in seen_links:
                seen_links.add(news['link'])
                unique_news.append(news)
        
        # Сортируем по дате (свежие первыми)
        unique_news.sort(key=lambda x: x.get('published', ''), reverse=True)
        
        return unique_news
    
    def get_fresh_news(self, all_news):
        """Получение только свежих новостей"""
        return [news for news in all_news if news['link'] not in self.posted_links]
    
    def mark_as_posted(self, link):
        """Помечаем новость как опубликованную"""
        self.posted_links.add(link)
        # Ограничиваем размер множества
        if len(self.posted_links) > 100:
            self.posted_links = set(list(self.posted_links)[-50:])
    
    async def close(self):
        """Закрытие сессии"""
        if self.session:
            await self.session.close()
