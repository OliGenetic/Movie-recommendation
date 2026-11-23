from telebot import types

def get_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("🎬 Подобрать фильм", callback_data="start_recommend"))
    return markup

def get_format_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Обычный фильм", callback_data="format_movie"),
        types.InlineKeyboardButton("Сериал", callback_data="format_tv"),
        types.InlineKeyboardButton("Мультфильм", callback_data="format_cartoon"),
        types.InlineKeyboardButton("Аниме", callback_data="format_anime"),
        types.InlineKeyboardButton("Дорама", callback_data="format_dorama")
    )
    return markup

def get_mood_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("😌 Расслабиться", callback_data="mood_relax"),
        types.InlineKeyboardButton("😱 Взбодриться", callback_data="mood_thrill"),
        types.InlineKeyboardButton("🤔 Подумать", callback_data="mood_think"),
        types.InlineKeyboardButton("😢 Поплакать", callback_data="mood_cry"),
        types.InlineKeyboardButton("🤷 Любое", callback_data="mood_any")
    )
    return markup

def get_year_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("2024-2020", callback_data="year_2020s"),
        types.InlineKeyboardButton("2019-2010", callback_data="year_2010s"),
        types.InlineKeyboardButton("2009-2000", callback_data="year_2000s"),
        types.InlineKeyboardButton("90-е", callback_data="year_1990s"),
        types.InlineKeyboardButton("80-е", callback_data="year_1980s"),
        types.InlineKeyboardButton("Любой", callback_data="year_any")
    )
    return markup

def get_country_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("США", callback_data="country_US"),
        types.InlineKeyboardButton("Россия", callback_data="country_RU"),
        types.InlineKeyboardButton("Ю. Корея", callback_data="country_KR"),
        types.InlineKeyboardButton("Япония", callback_data="country_JP"),
        types.InlineKeyboardButton("Франция", callback_data="country_FR"),
        types.InlineKeyboardButton("Индия", callback_data="country_IN"),
        types.InlineKeyboardButton("Великобритания", callback_data="country_GB"),
        types.InlineKeyboardButton("Германия", callback_data="country_DE"),
        types.InlineKeyboardButton("Любая", callback_data="country_any")
    )
    return markup

def get_theme_keyboard():
    # Используем ключевые слова (Keywords)
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("По играм", callback_data="theme_games"),
        types.InlineKeyboardButton("По комиксам", callback_data="theme_comics"),
        types.InlineKeyboardButton("Про роботов", callback_data="theme_robots"),
        types.InlineKeyboardButton("Про животных", callback_data="theme_animals"),
        types.InlineKeyboardButton("Любая тема", callback_data="theme_any")
    )
    return markup

def get_studio_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Marvel", callback_data="studio_420"),
        types.InlineKeyboardButton("DC", callback_data="studio_9993"),
        types.InlineKeyboardButton("Pixar", callback_data="studio_3"),
        types.InlineKeyboardButton("Netflix", callback_data="studio_213"),
        types.InlineKeyboardButton("Любая", callback_data="studio_any")
    )
    return markup

def get_skip_person_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⏭ Пропустить", callback_data="person_skip"))
    return markup

def get_extra_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Рейтинг 7+", callback_data="extra_rating"),
        types.InlineKeyboardButton("Короткометражка (<90м)", callback_data="extra_short"),
        types.InlineKeyboardButton("Долгий фильм (>150м)", callback_data="extra_long"),
        types.InlineKeyboardButton("Без ограничений", callback_data="extra_any")
    )
    return markup
