import aiohttp
import logging
from PIL import Image, ImageDraw, ImageFont
import io
import random

class ImageService:
    def __init__(self):
        self.colors = [
            (41, 128, 185),   # Синий
            (39, 174, 96),    # Зеленый
            (142, 68, 173),   # Фиолетовый
            (230, 126, 34),   # Оранжевый
            (231, 76, 60),    # Красный
            (52, 152, 219),   # Голубой
        ]
    
    async def generate_tech_image(self, title):
        """Генерация технологического изображения"""
        try:
            # Создаем изображение
            width, height = 800, 400
            bg_color = random.choice(self.colors)
            
            # Создаем базовое изображение
            image = Image.new('RGB', (width, height), color=bg_color)
            draw = ImageDraw.Draw(image)
            
            # Добавляем технологические элементы
            self._add_tech_elements(draw, width, height)
            
            # Добавляем текст
            self._add_title(draw, title, width, height)
            
            # Конвертируем в bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG', quality=85)
            img_byte_arr.seek(0)
            
            return img_byte_arr.getvalue()
            
        except Exception as e:
            logging.error(f"Image generation error: {e}")
            return None
    
    def _add_tech_elements(self, draw, width, height):
        """Добавляет технологические элементы на изображение"""
        # Круги
        for _ in range(5):
            x = random.randint(50, width - 50)
            y = random.randint(50, height - 50)
            radius = random.randint(10, 50)
            color = (255, 255, 255, 50)  # Полупрозрачный белый
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], outline=color, width=2)
        
        # Линии
        for _ in range(3):
            x1, y1 = random.randint(0, width), random.randint(0, height)
            x2, y2 = random.randint(0, width), random.randint(0, height)
            color = (255, 255, 255, 30)
            draw.line([x1, y1, x2, y2], fill=color, width=2)
    
    def _add_title(self, draw, title, width, height):
        """Добавляет заголовок на изображение"""
        try:
            # Разбиваем заголовок на строки
            words = title.split()
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                if len(test_line) <= 40:  # Ограничение по длине строки
                    current_line.append(word)
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Ограничиваем количество строк
            lines = lines[:3]
            
            # Рисуем строки
            font_size = 24 if len(lines) <= 2 else 20
            y_position = height // 2 - (len(lines) * font_size) // 2
            
            for i, line in enumerate(lines):
                # Тень
                draw.text(
                    (width//2 + 2, y_position + 2), 
                    line, 
                    fill=(0, 0, 0, 180),
                    font_size=font_size,
                    anchor="mm"
                )
                # Основной текст
                draw.text(
                    (width//2, y_position), 
                    line, 
                    fill=(255, 255, 255),
                    font_size=font_size,
                    anchor="mm"
                )
                y_position += font_size + 5
                
        except Exception as e:
            logging.error(f"Title drawing error: {e}")
