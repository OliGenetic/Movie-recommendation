import random 
import os
import threading
from fastapi import FastAPI
import uvicorn
import telebot
import config
import keyboards
import tmdb_api

# 1. FastAPI приложение для health check
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

# 2. Порт, который даёт Render (по умолчанию 10000)
port = int(os.environ.get("PORT", 10000))

# 3. Бот
bot = telebot.TeleBot(config.BOT_TOKEN)
user_states = {}

# Вспомогательная функция для отправки фильмов
def send_movies(chat_id, movies):
    for movie in movies:
        title = movie.get('title') or movie.get('name', 'Без названия')
        date = movie.get('release_date') or movie.get('first_air_date', '')
        year = date[:4] if date else '----'
        
        overview = movie.get('overview', '').strip()
        if not overview:
            overview = "😔 Описание отсутствует на русском языке."
        elif len(overview) > 800:
            overview = overview[:800].rsplit(' ', 1)[0] + "..."
        
        caption = (
            f"🎬 *{title}* ({year})\n"
            f"⭐ Рейтинг: {movie.get('vote_average', 0):.1f}\n\n"
            f"{overview}"
        )
        
        if movie.get('poster_path'):
            photo_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
            bot.send_photo(chat_id, photo_url, caption=caption, parse_mode='Markdown')
        else:
            bot.send_message(chat_id, caption, parse_mode='Markdown')

@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    user_states[chat_id] = {}
    bot.send_message(
        chat_id,
        f"Привет, {message.from_user.first_name}! 👋\n"
        "Я продвинутый бот-кинокритик. Задам несколько вопросов, чтобы подобрать идеальный фильм.",
        reply_markup=keyboards.get_main_menu()
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    data = call.data

    bot.answer_callback_query(call.id)
    state = user_states.get(chat_id, {})

    # 1. РАНДОМНЫЙ ПОИСК
    if data == "random_movie":
    bot.edit_message_text("🎲 Ищу случайный фильм, секунду...", chat_id, message_id)
    
    # Запрашиваем у TMDB популярные фильмы
    random_page = random.randint(1, 5) 
    params = {
        "api_key": config.TMDB_API_KEY,
        "language": "ru-RU",
        "sort_by": "popularity.desc",
        "vote_average.gte": 6.5,
        "vote_count.gte": 100,
        "page": random_page
    }
    url = "https://api.themoviedb.org/3/discover/movie"
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            random_movie = random.choice(results)
            send_movies(chat_id, [random_movie]) # Отправляем один фильм
            bot.send_message(chat_id, "Хочешь ещё один случайный фильм?", reply_markup=keyboards.get_random_keyboard())
        else:
            bot.send_message(chat_id, "Не удалось найти случайный фильм. Попробуйте позже.")
    else:
        bot.send_message(chat_id, "Ошибка при поиске. Попробуйте позже.")
    
    # 1. ЗАПУСК     
    if data == "start_recommend":
        user_states[chat_id] = {'page': 1} # Сбрасываем и задаем 1 страницу
        bot.edit_message_text("Шаг 1. Что будем смотреть?", chat_id, message_id, reply_markup=keyboards.get_format_keyboard())

    # 2. ФОРМАТ
    elif data.startswith("format_"):
        user_states[chat_id]['format'] = data.split("_")[1]
        bot.edit_message_text("Шаг 2. Под какое настроение?", chat_id, message_id, reply_markup=keyboards.get_mood_keyboard())

    # 3. НАСТРОЕНИЕ
    elif data.startswith("mood_"):
        user_states[chat_id]['mood'] = data.split("_")[1]
        bot.edit_message_text("Шаг 3. Выберите период выхода:", chat_id, message_id, reply_markup=keyboards.get_year_keyboard())

    # 4. ГОД
    elif data.startswith("year_"):
        user_states[chat_id]['year'] = data.split("_", 1)[1]
        bot.edit_message_text("Шаг 4. Страна производства:", chat_id, message_id, reply_markup=keyboards.get_country_keyboard())

    # 5. СТРАНА
    elif data.startswith("country_"):
        user_states[chat_id]['country'] = data.split("_")[1]
        bot.edit_message_text("Шаг 5. Основа сюжета:", chat_id, message_id, reply_markup=keyboards.get_plot_keyboard())

    # 6. ОСНОВА СЮЖЕТА
    elif data.startswith("plot_"):
        user_states[chat_id]['plot'] = data.split("_")[1]
        bot.edit_message_text("Шаг 6. Главные герои (персонажи):", chat_id, message_id, reply_markup=keyboards.get_character_keyboard())

    # 7. ПЕРСОНАЖИ
    elif data.startswith("char_"):
        user_states[chat_id]['char'] = data.split("_")[1]
        bot.edit_message_text("Шаг 7. Выберите минимальный рейтинг TMDB (1–10):", chat_id, message_id, reply_markup=keyboards.get_rating_keyboard())

    # 9. РЕЙТИНГ
    elif data.startswith("rating_"):
        user_states[chat_id]['rating'] = data.split("_")[1]
        bot.edit_message_text("Шаг 8. Длительность только для фильма:", chat_id, message_id, reply_markup=keyboards.get_runtime_keyboard())

   # 10. ДЛИТЕЛЬНОСТЬ (ПЕРВЫЙ ЗАПРОС)
    elif data.startswith("runtime_"):
        user_states[chat_id]['runtime'] = data.split("_")[1]
        bot.edit_message_text("🔎 Ищу подходящие варианты, секунду...", chat_id, message_id)
        
        movies, total_pages = tmdb_api.get_recommendations(user_states[chat_id], page=1)
        
        if not movies:
            bot.send_message(chat_id, "😔 Ничего не нашлось. Попробуйте убрать строгие фильтры через /start")
        else:
            bot.send_message(chat_id, f"🍿 Нашел варианты (Страница 1 из {total_pages}):")
            send_movies(chat_id, movies)
            
            # Если есть еще страницы, показываем кнопку
            if total_pages > 1:
                bot.send_message(chat_id, "Хотите посмотреть другие варианты?", reply_markup=keyboards.get_more_results_keyboard())
            else:
                bot.send_message(chat_id, "Больше ничего не нашли по вашему запросу. Нажмите /start, чтобы начать заново.")

    # ОБРАБОТКА КНОПКИ "ПОКАЗАТЬ ЕЩЁ"
    elif data == "more_results":
        # Увеличиваем номер страницы
        current_page = state.get('page', 1) + 1
        
        # Меняем текст сообщения с кнопкой на "Загрузка..."
        bot.edit_message_text("🔎 Ищу дальше...", chat_id, message_id)
        
        movies, total_pages = tmdb_api.get_recommendations(state, page=current_page)
        
        if not movies:
            bot.send_message(chat_id, 
                             "😔 Ничего не нашлось. Попробуйте изменить фильтры или посмотрите случайный фильм.", 
        reply_markup=keyboards.get_random_keyboard() 
        )
        else:
            user_states[chat_id]['page'] = current_page
            bot.send_message(chat_id, f"🍿 Страница {current_page} из {total_pages}:")
            send_movies(chat_id, movies)
            
            # Если это была последняя страница, убираем кнопку
            if current_page >= total_pages:
                bot.edit_message_text("Это все фильмы, которые мы нашли.", chat_id, message_id)
            else:
                bot.edit_message_text("Хотите посмотреть другие варианты?", chat_id, message_id, reply_markup=keyboards.get_more_results_keyboard())

# 4. Запуск бота в отдельном потоке
def run_bot():
    print("Удаляю возможный вебхук и старые обновления...")
    # drop_pending_updates=True сбрасывает накопившиеся сообщения и убивает старые сессии
    bot.delete_webhook(drop_pending_updates=True) 
    print("Бот запущен и готов к работе!")
    # Добавляем запрос на получение обновлений с параметром skip_pending
    bot.infinity_polling(skip_pending=True, timeout=20, long_polling_timeout=20)

# 5. Точка входа
if __name__ == "__main__":
    # Запускаем бота в фоновом потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Запускаем FastAPI в основном потоке (чтобы Render видел порт)
    print(f"Запуск FastAPI на порту {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
