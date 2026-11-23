import telebot
from telebot import types
import config
import keyboards
import tmdb_api

# Инициализация бота
bot = telebot.TeleBot(config.BOT_TOKEN)

# Словарь для хранения состояний пользователей (в оперативной памяти)
# В реальном проекте используют базу данных (например, Redis или SQLite)
user_states = {}

# --- ОБРАБОТЧИК КОМАНДЫ /start ---
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    # Сбрасываем состояние при старте
    user_states[chat_id] = {}
    
    bot.send_message(
        chat_id,
        f"Привет, {message.from_user.first_name}! 👋\n"
        "Я бот-кинокритик. Помогу подобрать фильм под твое настроение.",
        reply_markup=keyboards.get_main_menu()
    )

# --- ОБРАБОТЧИК INLINE-КНОПОК ---
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    data = call.data

    # Обязательно отвечаем на колбэк, чтобы убрать "часики" с кнопки
    bot.answer_callback_query(call.id)

    # 1. Запуск подбора
    if data == "start_recommend":
        user_states[chat_id] = {'step': 'year'}
        bot.edit_message_text(
            "Шаг 1 из 5. Выберите год выпуска:",
            chat_id, message_id, reply_markup=keyboards.get_year_keyboard()
        )

    # 2. Выбор года
    elif data.startswith("year_"):
        year_val = data.split("_")[1]
        user_states[chat_id]['year'] = year_val
        user_states[chat_id]['step'] = 'genre'
        
        bot.edit_message_text(
            "Шаг 2 из 5. Выберите жанр:",
            chat_id, message_id, reply_markup=keyboards.get_genre_keyboard()
        )

    # 3. Выбор жанра
    elif data.startswith("genre_"):
        genre_id = data.split("_")[1]
        user_states[chat_id]['genre'] = genre_id
        user_states[chat_id]['step'] = 'mood'
        
        bot.edit_message_text(
            "Шаг 3 из 5. Какое у вас настроение?",
            chat_id, message_id, reply_markup=keyboards.get_mood_keyboard()
        )

    # 4. Выбор настроения
    elif data.startswith("mood_"):
        mood_val = data.split("_")[1]
        user_states[chat_id]['mood'] = mood_val
        user_states[chat_id]['step'] = 'actor'
        
        bot.edit_message_text(
            "Шаг 4 из 5. Введите имя актера (или нажмите кнопку «Пропустить»):",
            chat_id, message_id, reply_markup=keyboards.get_skip_actor_keyboard()
        )

    # Обработка кнопки "Пропустить актера"
    elif data == "skip_actor":
        user_states[chat_id]['actor'] = None
        user_states[chat_id]['step'] = 'country'
        
        bot.edit_message_text(
            "Шаг 5 из 5. Выберите страну производства:",
            chat_id, message_id, reply_markup=keyboards.get_country_keyboard()
        )

    # 5. Выбор страны и ФИНАЛ (отправка запроса к TMDB)
    elif data.startswith("country_"):
        country_code = data.split("_")[1]
        user_states[chat_id]['country'] = country_code
        
        # Меняем сообщение на "Загрузка..."
        bot.edit_message_text("🔎 Ищу подходящие фильмы, секунду...", chat_id, message_id)
        
        # Достаем все данные пользователя
        state = user_states[chat_id]
        
        # Делаем запрос к TMDB (функция из tmdb_api.py)
        movies = tmdb_api.get_movies(
            year=state.get('year'),
            genre_id=state.get('genre'),
            mood=state.get('mood'),
            country=state.get('country'),
            actor_name=state.get('actor')
        )
        
        # Отправляем результаты
        if not movies:
            bot.send_message(chat_id, "😔 Ничего не нашлось по вашим критериям. Попробуйте изменить параметры через /start")
        else:
            bot.send_message(chat_id, f"🍿 Нашел {len(movies)} вариантов! Вот они:")
            for movie in movies:
                # Формируем карточку фильма
                caption = (
                    f"🎬 *{movie['title']}* ({movie.get('release_date', '')[:4]})\n"
                    f"⭐ Рейтинг: {movie.get('vote_average', 0):.1f}\n\n"
                    f"{movie.get('overview', 'Описание отсутствует.')[:300]}..."
                )
                
                # Отправляем постер, если он есть
                if movie.get('poster_path'):
                    photo_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                    bot.send_photo(chat_id, photo_url, caption=caption, parse_mode='Markdown')
                else:
                    bot.send_message(chat_id, caption, parse_mode='Markdown')
        
        # Очищаем состояние после выдачи
        user_states[chat_id] = {}
        bot.send_message(chat_id, "Чтобы начать заново, нажмите /start")

# --- ОБРАБОТЧИК ТЕКСТА (Ввод актера) ---
@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('step') == 'actor')
def handle_actor_input(message):
    chat_id = message.chat.id
    actor_name = message.text
    
    # Сохраняем имя актера
    user_states[chat_id]['actor'] = actor_name
    user_states[chat_id]['step'] = 'country'
    
    bot.send_message(
        chat_id,
        f"Принято! Ищу фильмы с {actor_name}.\nШаг 5 из 5. Выберите страну производства:",
        reply_markup=keyboards.get_country_keyboard()
    )

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен и готов к работе!")
    bot.infinity_polling()
