from telebot import types

def get_random_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎲 Рекомендация рандомного фильма", callback_data="random_movie"))
    return markup

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
        types.InlineKeyboardButton("Дорама", callback_data="format_dorama"),
        types.InlineKeyboardButton("🎲 Любой фильм", callback_data="format_any")
    )
    return markup

def get_mood_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("😌 Расслабиться", callback_data="mood_relax"),
        types.InlineKeyboardButton("😱 Взбодриться", callback_data="mood_thrill"),
        types.InlineKeyboardButton("🤔 Подумать", callback_data="mood_think"),
        types.InlineKeyboardButton("😢 Поплакать", callback_data="mood_cry"),
        types.InlineKeyboardButton("☁️ Помечтать", callback_data="mood_dream"),
        types.InlineKeyboardButton("😂 Посмеяться", callback_data="mood_laugh"),
        types.InlineKeyboardButton("❤️ Романтика", callback_data="mood_romance"),
        types.InlineKeyboardButton("🎲 Любой фильм", callback_data="mood_any")
    )
    return markup

def get_year_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("2025-2026", callback_data="year_2025_2026"),
        types.InlineKeyboardButton("2020-2024", callback_data="year_2020_2024"),
        types.InlineKeyboardButton("2015-2019", callback_data="year_2015_2019"),
        types.InlineKeyboardButton("2010-2014", callback_data="year_2010_2014"),
        types.InlineKeyboardButton("2000-2009", callback_data="year_2000_2009"),
        types.InlineKeyboardButton("90-е", callback_data="year_1990_1999"),
        types.InlineKeyboardButton("80-е", callback_data="year_1980_1989"),
        types.InlineKeyboardButton("🎲 Любой фильм", callback_data="year_any")
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
        types.InlineKeyboardButton("Великобритания", callback_data="country_GB"),
        types.InlineKeyboardButton("Китай", callback_data="country_CN"),
        types.InlineKeyboardButton("Турция", callback_data="country_TR"),
        types.InlineKeyboardButton("Индия", callback_data="country_IN"),
        types.InlineKeyboardButton("Италия", callback_data="country_IT"),
        types.InlineKeyboardButton("Испания", callback_data="country_ES"),
        types.InlineKeyboardButton("🎲 Любой фильм", callback_data="country_any")
    )
    return markup

def get_plot_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🎮 По играм", callback_data="plot_games"),
        types.InlineKeyboardButton("🦸 По комиксам", callback_data="plot_comics"),
        types.InlineKeyboardButton("📖 По книгам", callback_data="plot_books"),
        types.InlineKeyboardButton("🎲 Любой фильм", callback_data="plot_any")
    )
    return markup

def get_character_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👨‍👩‍👧‍👧 Про людей", callback_data="char_people"), # НОВОЕ
        types.InlineKeyboardButton("🤖 Про роботов", callback_data="char_robots"),
        types.InlineKeyboardButton("🦊 Про животных", callback_data="char_animals"),
        types.InlineKeyboardButton("👽 Про инопланетян", callback_data="char_aliens"),
        types.InlineKeyboardButton("🧛 Про вампиров", callback_data="char_vampires"),
        types.InlineKeyboardButton("🎲 Любой фильм", callback_data="char_any")
    )
    return markup

def get_rating_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Рейтинг 8+", callback_data="rating_8"),
        types.InlineKeyboardButton("Рейтинг 7+", callback_data="rating_7"),
        types.InlineKeyboardButton("Рейтинг 6+", callback_data="rating_6"), # НОВОЕ
        types.InlineKeyboardButton("🎲 Любой фильм", callback_data="rating_any")
    )
    return markup

def get_runtime_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Короткий (<90 минут)", callback_data="runtime_short"),
        types.InlineKeyboardButton("Средний (90-150 минут)", callback_data="runtime_medium"),
        types.InlineKeyboardButton("Долгий (>150 минут)", callback_data="runtime_long"),
        types.InlineKeyboardButton("🎲 Любой фильм", callback_data="runtime_any")
    )
    return markup

def get_more_results_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⏩ Показать ещё", callback_data="more_results"))
    return markup

def get_restart_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔄 Повторить поиск", callback_data="start_recommend"))
    return markup
