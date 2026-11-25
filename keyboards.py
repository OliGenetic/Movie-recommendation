from telebot import types

# Inline-кнопки
def get_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🎬 Подобрать фильм", callback_data="start_recommend"),
        types.InlineKeyboardButton("🎲 Случайный фильм", callback_data="random_movie")
    )
    return markup

def get_random_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎲 Ещё случайный фильм", callback_data="random_movie"))
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
        types.InlineKeyboardButton("🎲 Любой год", callback_data="year_any")
    )
    return markup

def get_country_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("США", callback_data="country_US"),
        types.InlineKeyboardButton("Россия", callback_data="country_RU"),
        types.InlineKeyboardButton("Канада", callback_data="country_CA"),
        types.InlineKeyboardButton("Великобритания", callback_data="country_GB"),
        types.InlineKeyboardButton("Франция", callback_data="country_FR"),
        types.InlineKeyboardButton("Германия", callback_data="country_DE"),
        types.InlineKeyboardButton("Италия", callback_data="country_IT"),
        types.InlineKeyboardButton("Испания", callback_data="country_ES"),
        types.InlineKeyboardButton("Исландия", callback_data="country_IS"),
        types.InlineKeyboardButton("Индия", callback_data="country_IN"),
        types.InlineKeyboardButton("Австралия", callback_data="country_AU"),
        types.InlineKeyboardButton("Бразилия", callback_data="country_BR"),
        types.InlineKeyboardButton("Ю. Корея", callback_data="country_KR"),
        types.InlineKeyboardButton("Япония", callback_data="country_JP"),
        types.InlineKeyboardButton("Китай", callback_data="country_CN"),
        types.InlineKeyboardButton("🎲 Любая", callback_data="country_any")
    )
    return markup

# СПЕЦИАЛЬНАЯ КЛАВИАТУРА ДЛЯ ДОРАМ
def get_dorama_country_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Ю. Корея", callback_data="country_KR"),
        types.InlineKeyboardButton("Япония", callback_data="country_JP"),
        types.InlineKeyboardButton("Китай", callback_data="country_CN"),
        types.InlineKeyboardButton("Тайвань", callback_data="country_TW"),
        types.InlineKeyboardButton("🎲 Любая из них", callback_data="country_any")
    )
    return markup

def get_plot_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🎮 По играм", callback_data="plot_games"),
        types.InlineKeyboardButton("🦸 По комиксам", callback_data="plot_comics"),
        types.InlineKeyboardButton("📖 По книгам", callback_data="plot_books"),
        types.InlineKeyboardButton("🎲 Любая", callback_data="plot_any")
    )
    return markup

def get_character_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👨‍👩‍👧‍👧 Про людей", callback_data="char_people"),
        types.InlineKeyboardButton("🤖 Про роботов", callback_data="char_robots"),
        types.InlineKeyboardButton("🦊 Про животных", callback_data="char_animals"),
        types.InlineKeyboardButton("👽 Про инопланетян", callback_data="char_aliens"),
        types.InlineKeyboardButton("🧛 Про вампиров", callback_data="char_vampires"),
        types.InlineKeyboardButton("🎲 Любые", callback_data="char_any")
    )
    return markup

def get_rating_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Рейтинг 8+", callback_data="rating_8"),
        types.InlineKeyboardButton("Рейтинг 7+", callback_data="rating_7"),
        types.InlineKeyboardButton("Рейтинг 6+", callback_data="rating_6"),
        types.InlineKeyboardButton("🎲 Любой", callback_data="rating_any")
    )
    return markup

def get_runtime_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Короткий (<90 мин)", callback_data="runtime_short"),
        types.InlineKeyboardButton("Средний (90-150 мин)", callback_data="runtime_medium"),
        types.InlineKeyboardButton("Долгий (>150 мин)", callback_data="runtime_long"),
        types.InlineKeyboardButton("🎲 Любой", callback_data="runtime_any")
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

# Reply-клавиатура (внизу экрана)
def get_reply_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_search = types.KeyboardButton("🎬 Подобрать фильм")
    btn_random = types.KeyboardButton("🎲 Случайный фильм")
    btn_new_year = types.KeyboardButton("🎄☃️✨ Новогодние фильмы")
    markup.add(btn_search, btn_random, btn_new_year)
    return markup
