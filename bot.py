import telebot
from telebot import types
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
        bot.edit_message_text("Шаг 2. Какое у Вас настроение?:", chat_id, message_id, reply_markup=keyboards.get_mood_keyboard())

    # 3. НАСТРОЕНИЕ
    elif data.startswith("mood_"):
        user_states[chat_id]['mood'] = data.split("_")[1]
        bot.edit_message_text("Шаг 3. Выберите десятилетие:", chat_id, message_id, reply_markup=keyboards.get_year_keyboard())

    # 4. ГОД
    elif data.startswith("year_"):
        user_states[chat_id]['year'] = data.split("_")[1]
        bot.edit_message_text("Шаг 4. Страна производства:", chat_id, message_id, reply_markup=keyboards.get_country_keyboard())

    # 5. СТРАНА
    elif data.startswith("country_"):
        user_states[chat_id]['country'] = data.split("_")[1]
        bot.edit_message_text("Шаг 5. Основа сюжета или персонажи:", chat_id, message_id, reply_markup=keyboards.get_theme_keyboard())

    # 6. ТЕМА (Персонажи / Источник)
    elif data.startswith("theme_"):
        user_states[chat_id]['theme'] = data.split("_")[1]
        bot.edit_message_text("Шаг 6. Выберите киностудию:", chat_id, message_id, reply_markup=keyboards.get_studio_keyboard())

    # 7. СТУДИЯ
    elif data.startswith("studio_"):
        user_states[chat_id]['studio'] = data.split("_")[1]
        user_states[chat_id]['step'] = 'person'
        bot.edit_message_text("Шаг 7. Введите имя актера или режиссера (например, Леонардо ДиКаприо), либо нажмите Пропустить:", chat_id, message_id, reply_markup=keyboards.get_skip_person_keyboard())

    # ОБРАБОТКА КНОПКИ ПРОПУСТИТЬ АКТЕРА
    elif data == "person_skip":
        user_states[chat_id]['person'] = None
        bot.edit_message_text("Шаг 8. Дополнительные фильтры:", chat_id, message_id, reply_markup=keyboards.get_extra_keyboard())

    # 8. ДОПОЛНИТЕЛЬНО (Рейтинг / Длительность)
    elif data.startswith("extra_"):
        user_states[chat_id]['extra'] = data.split("_")[1]
        bot.edit_message_text("🔎 Ищу подходящие варианты, секунду...", chat_id, message_id)
        
        # ЗАПРОС К API
        movies = tmdb_api.get_recommendations(user_states[chat_id])
        
        if not movies:
            bot.send_message(chat_id, "😔 Ничего не нашлось. Попробуйте убрать актера или изменить фильтры через /start")
        else:
            bot.send_message(chat_id, f"🍿 Нашел {len(movies)} вариантов:")
            for movie in movies:
                title = movie.get('title') or movie.get('name', 'Без названия')
                date = movie.get('release_date') or movie.get('first_air_date', '')
                year = date[:4] if date else '----'
                
                # Получаем описание
                overview = movie.get('overview', 'Описание отсутствует.')
                
                # Если описание длиннее 800 символов, аккуратно обрезаем его по последнему пробелу
                if len(overview) > 800:
                    overview = overview[:800].rsplit(' ', 1)[0] + "..."
                
                caption = (
                    f"🎬 *{title}* ({year})\n"
                    f"⭐ Рейтинг: {movie.get('vote_average', 0):.1f}\n\n"
                    f"{overview}"
                )
                
                # Отправляем постер
                if movie.get('poster_path'):
                    photo_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                    bot.send_photo(chat_id, photo_url, caption=caption, parse_mode='Markdown')
                else:
                    bot.send_message(chat_id, caption, parse_mode='Markdown')
        
        user_states[chat_id] = {}
        bot.send_message(chat_id, "Чтобы начать заново, нажмите /start")

# ВВОД АКТЕРА / РЕЖИССЕРА
@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('step') == 'person')
def handle_person_input(message):
    chat_id = message.chat.id
    user_states[chat_id]['person'] = message.text
    user_states[chat_id]['step'] = None
    
    bot.send_message(
        chat_id,
        f"Принято! Ищу с участием/режиссурой: {message.text}.\nШаг 8. Дополнительные фильтры:",
        reply_markup=keyboards.get_extra_keyboard()
    )

if __name__ == "__main__":
    print("Бот запущен и готов к работе!")
    bot.infinity_polling()
