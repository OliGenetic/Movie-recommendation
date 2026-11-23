from telebot import types

def get_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("🎬 Подобрать фильм", callback_data="start_recommend"))
    return markup

def get_year_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("2024", callback_data="year_2024"),
        types.InlineKeyboardButton("2023", callback_data="year_2023"),
        types.InlineKeyboardButton("2020-е", callback_data="year_2020s"),
        types.InlineKeyboardButton("2010-е", callback_data="year_2010s"),
        types.InlineKeyboardButton("Любой", callback_data="year_any")
    )
    return markup

def get_genre_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    # ID жанров взяты из TMDB API
    markup.add(
        types.InlineKeyboardButton("Боевик", callback_data="genre_28"),
        types.InlineKeyboardButton("Комедия", callback_data="genre_35"),
        types.InlineKeyboardButton("Драма", callback_data="genre_18"),
        types.InlineKeyboardButton("Фантастика", callback_data="genre_878"),
        types.InlineKeyboardButton("Ужасы", callback_data="genre_27")
    )
    return markup

def get_mood_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("😌 Расслабиться", callback_data="mood_relax"),
        types.InlineKeyboardButton("😱 Пощекотать нервы", callback_data="mood_thrill"),
        types.InlineKeyboardButton("🤔 Подумать о жизни", callback_data="mood_think")
    )
    return markup

def get_skip_actor_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⏭ Пропустить", callback_data="skip_actor"))
    return markup

def get_country_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    # Коды стран по стандарту ISO
    markup.add(
        types.InlineKeyboardButton("США", callback_data="country_US"),
        types.InlineKeyboardButton("Россия", callback_data="country_RU"),
        types.InlineKeyboardButton("Франция", callback_data="country_FR"),
        types.InlineKeyboardButton("Южная Корея", callback_data="country_KR"),
        types.InlineKeyboardButton("Любая", callback_data="country_any")
    )
    return markup
