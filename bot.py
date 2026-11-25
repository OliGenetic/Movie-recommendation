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

# 2. Порт
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

        # Если русского описания нет — запрашиваем английское
        if not overview:
            is_tv = 'name' in movie 
            overview = tmdb_api.get_english_overview(movie.get('id'), is_tv=is_tv)

        # Если и на английском ничего нет, ставим заглушку
        if not overview:
            overview = "😔 Описание отсутствует на доступных языках."

        # Обрезаем текст, если он слишком длинный (лимит Telegram 1024 символа)
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
    user_states[chat_id] = {}  # хранение выбора пользователя

    # Отправляем приветствие и постоянную клавиатуру
    bot.send_message(
        chat_id,
        f"Привет, {message.from_user.first_name}! 👋\n"
        "Я продвинутый бот-кинокритик 🎥 FilmStart 🎥\n"
        "Задам несколько вопросов, чтобы подобрать идеальный фильм.",
        reply_markup=keyboards.get_reply_main_menu()
    )

# Обработчик для кнопки "Подобрать фильм"
@bot.message_handler(func=lambda message: message.text == "🎬 Подобрать фильм")
def handle_search_btn(message):
    chat_id = message.chat.id
    user_states[chat_id] = {'page': 1}

    # Отправляем первое сообщение опроса с Inline-кнопками
    bot.send_message(chat_id, "Что будем смотреть?", reply_markup=keyboards.get_format_keyboard())

# Обработчик для кнопки "Случайный фильм"
@bot.message_handler(func=lambda message: message.text == "🎲 Случайный фильм")
def handle_random_btn(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "🎲 Ищу случайный фильм, секунду...")
    random_movie = tmdb_api.get_random_movie()
    
    if random_movie:
        send_movies(chat_id, [random_movie])
        bot.send_message(chat_id, "Хочешь ещё один?", reply_markup=keyboards.get_random_keyboard())
    else:
        bot.send_message(chat_id, "😔 Не удалось найти фильм. Попробуйте позже.")

# Поиск новогоднего фильма
@bot.message_handler(func=lambda message: "Новогодние фильмы" in message.text)
def handle_new_year_btn(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "🎄 Ищу лучшие новогодние фильмы...")
    movies = tmdb_api.get_new_year_movies()
    
    if movies:
        send_movies(chat_id, movies)
        # Отправляем кнопку, чтобы можно было продолжить
        bot.send_message(chat_id, "Хотите посмотреть ещё?", reply_markup=keyboards.get_more_results_keyboard())
    else:
        bot.send_message(chat_id, "😔 Не удалось найти новогодние фильмы.")

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
        random_movie = tmdb_api.get_random_movie()
        if random_movie:
            send_movies(chat_id, [random_movie])
            bot.send_message(chat_id, "Хочешь ещё один?", reply_markup=keyboards.get_random_keyboard())
        else:
            bot.send_message(chat_id, "😔 Не удалось найти фильм. Попробуйте позже.", reply_markup=keyboards.get_restart_keyboard())

    # 2. ЗАПУСК ОПРОСА
    elif data == "start_recommend":
        user_states[chat_id] = {'page': 1}
        bot.edit_message_text("Что будем смотреть?", chat_id, message_id, reply_markup=keyboards.get_format_keyboard())

    # 3. ФОРМАТ
    elif data.startswith("format_"):
        user_states[chat_id]['format'] = data.split("_")[1]
        bot.edit_message_text("Под какое настроение?", chat_id, message_id, reply_markup=keyboards.get_mood_keyboard())

    # 4. НАСТРОЕНИЕ
    elif data.startswith("mood_"):
        user_states[chat_id]['mood'] = data.split("_")[1]
        bot.edit_message_text("Выберите период выхода:", chat_id, message_id, reply_markup=keyboards.get_year_keyboard())

    # 5. ГОД
    elif data.startswith("year_"):
        user_states[chat_id]['year'] = data.split("_", 1)[1]
        fmt = user_states[chat_id].get('format')
        
        if fmt == 'anime':
            # Пропускаем выбор страны для аниме
            bot.edit_message_text("Основа сюжета:", chat_id, message_id, reply_markup=keyboards.get_plot_keyboard())
        elif fmt == 'dorama':
            # Специальная клавиатура для дорам
            bot.edit_message_text("Страна производства (для дорам):", chat_id, message_id, reply_markup=keyboards.get_dorama_country_keyboard())
        else:
            bot.edit_message_text("Страна производства:", chat_id, message_id, reply_markup=keyboards.get_country_keyboard())

    # 6. СТРАНА
    elif data.startswith("country_"):
        user_states[chat_id]['country'] = data.split("_")[1]
        bot.edit_message_text("Основа сюжета:", chat_id, message_id, reply_markup=keyboards.get_plot_keyboard())

    # 7. ОСНОВА СЮЖЕТА
    elif data.startswith("plot_"):
        user_states[chat_id]['plot'] = data.split("_")[1]
        bot.edit_message_text("Главные герои (персонажи):", chat_id, message_id, reply_markup=keyboards.get_character_keyboard())

    # 8. ПЕРСОНАЖИ
    elif data.startswith("char_"):
        user_states[chat_id]['char'] = data.split("_")[1]
        bot.edit_message_text("Выберите минимальный рейтинг:", chat_id, message_id, reply_markup=keyboards.get_rating_keyboard())

    # 9. РЕЙТИНГ
    elif data.startswith("rating_"):
        user_states[chat_id]['rating'] = data.split("_")[1]
        fmt = user_states[chat_id].get('format')

        # Длительность только для обычных фильмов 
        if fmt == 'movie':
            bot.edit_message_text("Длительность фильма:", chat_id, message_id, reply_markup=keyboards.get_runtime_keyboard())
        else:
            # Для остальных форматов сразу запускаем поиск
            bot.edit_message_text("🔎 Ищу подходящие варианты, секунду...", chat_id, message_id)
            user_states[chat_id]['page'] = 1
            movies, total_pages = tmdb_api.get_recommendations(user_states[chat_id], page=1)
            
            if not movies:
                bot.send_message(chat_id, "😔 Ничего не нашлось. Попробуйте изменить фильтры.", reply_markup=keyboards.get_restart_keyboard())
            else:
                bot.send_message(chat_id, f"🍿 Нашел варианты (Страница 1 из {total_pages}):")
                send_movies(chat_id, movies)
                if total_pages > 1:
                    # Отправляем кнопку НОВЫМ сообщением, чтобы она всегда была внизу
                    bot.send_message(chat_id, "Хотите посмотреть другие варианты?", reply_markup=keyboards.get_more_results_keyboard())
                else:
                    bot.send_message(chat_id, "Больше ничего не нашли по данному запросу.", reply_markup=keyboards.get_restart_keyboard())

    elif data.startswith("runtime_"):
        user_states[chat_id]['runtime'] = data.split("_")[1]
        bot.edit_message_text("🔎 Ищу подходящие варианты, секунду...", chat_id, message_id)
        
        user_states[chat_id]['page'] = 1
        movies, total_pages = tmdb_api.get_recommendations(user_states[chat_id], page=1)
        
        if not movies:
            bot.send_message(chat_id, "😔 Ничего не нашлось. Попробуйте изменить фильтры.", reply_markup=keyboards.get_restart_keyboard())
        else:
            bot.send_message(chat_id, f"🍿 Нашел варианты (Страница 1 из {total_pages}):")
            send_movies(chat_id, movies)
            if total_pages > 1:
                bot.send_message(chat_id, "Хотите посмотреть другие варианты?", reply_markup=keyboards.get_more_results_keyboard())
            else:
                bot.send_message(chat_id, "Больше ничего не нашли по данному запросу.", reply_markup=keyboards.get_restart_keyboard())

    # Пагинация ("Показать ещё")
    elif data == "more_results":
        current_page = state.get('page', 1) + 1
        
        if current_page > 500:
            bot.edit_message_text("Достигнут лимит выдачи. Начните новый поиск.", chat_id, message_id, reply_markup=keyboards.get_restart_keyboard())
            return

        # Удаляем старое сообщение с кнопкой
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass
        
        loading_msg = bot.send_message(chat_id, f"🔎 Ищу страницу {current_page}...")
        movies, total_pages = tmdb_api.get_recommendations(state, page=current_page)
        
        if not movies:
            bot.edit_message_text("😔 Больше ничего не нашли.", chat_id, loading_msg.message_id, reply_markup=keyboards.get_restart_keyboard())
        else:
            user_states[chat_id]['page'] = current_page
            bot.delete_message(chat_id, loading_msg.message_id)
            bot.send_message(chat_id, f"🍿 Страница {current_page} из {total_pages}:")
            send_movies(chat_id, movies)
            
            # Всегда отправляем новую кнопку внизу, пока не дошли до конца
            if current_page >= total_pages:
                bot.send_message(chat_id, "Это все фильмы, которые удалось найти.", reply_markup=keyboards.get_restart_keyboard())
            else:
                bot.send_message(chat_id, "Хотите посмотреть другие варианты?", reply_markup=keyboards.get_more_results_keyboard())

def run_bot():
    bot.delete_webhook(drop_pending_updates=True) 
    bot.infinity_polling(skip_pending=True, timeout=20, long_polling_timeout=20)

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=port)
