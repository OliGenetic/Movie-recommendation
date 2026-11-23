import telebot
import config
import keyboards
import tmdb_api

bot = telebot.TeleBot(config.BOT_TOKEN)
user_states = {}

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

    # 1. ЗАПУСК
    if data == "start_recommend":
        user_states[chat_id] = {}
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
        bot.edit_message_text("Шаг 7. Выберите киностудию:", chat_id, message_id, reply_markup=keyboards.get_studio_keyboard())

    # 8. СТУДИЯ (сразу переходим к рейтингу)
    elif data.startswith("studio_"):
        user_states[chat_id]['studio'] = data.split("_")[1]
        bot.edit_message_text("Шаг 8. Выберите минимальный рейтинг:", chat_id, message_id, reply_markup=keyboards.get_rating_keyboard())

    # 9. РЕЙТИНГ (переходим к длительности)
    elif data.startswith("rating_"):
        user_states[chat_id]['rating'] = data.split("_")[1]
        bot.edit_message_text("Шаг 9. Длительность фильма:", chat_id, message_id, reply_markup=keyboards.get_runtime_keyboard())

    # 10. ДЛИТЕЛЬНОСТЬ (ФИНАЛ)
    elif data.startswith("runtime_"):
        user_states[chat_id]['runtime'] = data.split("_")[1]
        bot.edit_message_text("🔎 Ищу подходящие варианты, секунду...", chat_id, message_id)
        
        # ЗАПРОС К API
        movies = tmdb_api.get_recommendations(user_states[chat_id])
        
        if not movies:
            bot.send_message(chat_id, "😔 Ничего не нашлось. Попробуйте убрать строгие фильтры (например, студию) через /start")
        else:
            bot.send_message(chat_id, f"🍿 Нашел {len(movies)} вариантов:")
            for movie in movies:
                title = movie.get('title') or movie.get('name', 'Без названия')
                date = movie.get('release_date') or movie.get('first_air_date', '')
                year = date[:4] if date else '----'
                
                overview = movie.get('overview', 'Описание отсутствует.')
                if len(overview) > 800:
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
        
        user_states[chat_id] = {}
        bot.send_message(chat_id, "Чтобы начать заново, нажмите /start")

if __name__ == "__main__":
    print("Бот запущен и готов к работе!")
    bot.infinity_polling()
