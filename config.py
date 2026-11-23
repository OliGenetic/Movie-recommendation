import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Читаем их
BOT_TOKEN = os.getenv("BOT_TOKEN")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Для проверки (выведем в консоль, чтобы убедиться, что токен есть)
if not BOT_TOKEN:
    print("ОШИБКА: BOT_TOKEN не найден в файле .env! Проверьте файл .env")
else:
    print("Токен Telegram успешно загружен из .env")
    
if not TMDB_API_KEY:
    print("ОШИБКА: TMDB_API_KEY не найден в файле .env!")
else:
    print("Ключ TMDB успешно загружен из .env")
