import requests
import config

BASE_URL = "https://api.themoviedb.org/3"

# ID ключевых слов (Keywords) из TMDB
KEYWORDS = {
    "games": "152368",   # based on video game
    "comics": "9715",    # based on comic book
    "robots": "11035",   # robot
    "animals": "14760"   # animal
}

def get_recommendations(state):
    # Определяем тип контента (фильм или сериал)
    media_type = "movie"
    if state.get('format') in ['tv', 'dorama', 'anime']:
        media_type = "tv"
    
    url = f"{BASE_URL}/discover/{media_type}"
    
    params = {
        "api_key": config.TMDB_API_KEY,
        "language": "ru-RU",
        "sort_by": "popularity.desc",
        "page": 1
    }

    # 1. ФОРМАТ (Спец. обработка)
    fmt = state.get('format')
    if fmt == 'cartoon':
        params["with_genres"] = "16" # Анимация
    elif fmt == 'anime':
        params["with_genres"] = "16"
        params["with_keywords"] = "210024" # Anime
    elif fmt == 'dorama':
        params["with_origin_country"] = "KR"

    # 2. НАСТРОЕНИЕ (Заменяет жанр)
    mood = state.get('mood')
    mood_genres = []
    if mood == "relax":
        mood_genres = ["35", "10751"]  # Комедия, Семейный
    elif mood == "thrill":
        mood_genres = ["28", "53", "27"] # Боевик, Триллер, Ужасы
    elif mood == "think":
        mood_genres = ["878", "9648"]  # Фантастика, Детектив
    elif mood == "cry":
        mood_genres = ["18", "10749"]  # Драма, Романтика
    
    # Объединяем жанры формата и настроения
    if mood_genres:
        if "with_genres" in params:
            params["with_genres"] += "," + ",".join(mood_genres)
        else:
            params["with_genres"] = ",".join(mood_genres)

    # 3. ГОД
    year = state.get('year')
    if year != "any":
        start_year = int(year[:4])
        end_year = start_year + 9
        if media_type == "movie":
            params["primary_release_date.gte"] = f"{start_year}-01-01"
            params["primary_release_date.lte"] = f"{end_year}-12-31"
        else:
            params["first_air_date.gte"] = f"{start_year}-01-01"
            params["first_air_date.lte"] = f"{end_year}-12-31"

    # 4. СТРАНА
    country = state.get('country')
    if country != "any":
        params["with_origin_country"] = country

    # 5. ТЕМА / ПЕРСОНАЖИ (Keywords)
    theme = state.get('theme')
    if theme in KEYWORDS:
        if "with_keywords" in params:
            params["with_keywords"] += "|" + KEYWORDS[theme] # Оператор | означает ИЛИ
        else:
            params["with_keywords"] = KEYWORDS[theme]

    # 6. СТУДИЯ (Companies)
    studio = state.get('studio')
    if studio != "any":
        params["with_companies"] = studio

    # 7. АКТЕР / РЕЖИССЕР
    person = state.get('person')
    if person and media_type == "movie": # Для сериалов TMDB не поддерживает поиск по актерам в discover
        search_url = f"{BASE_URL}/search/person"
        res = requests.get(search_url, params={"api_key": config.TMDB_API_KEY, "query": person}).json()
        if res.get("results"):
            person_id = res["results"][0]["id"]
            # Ищем и как актера (with_cast), и как режиссера (with_crew)
            params["with_cast"] = person_id
    elif person and media_type == "tv":
        print("Предупреждение: TMDB не поддерживает фильтр по актерам для сериалов в discover.")

    # 8. ДОПОЛНИТЕЛЬНО (Рейтинг / Длительность)
    extra = state.get('extra')
    if extra == "rating":
        params["vote_average.gte"] = 7.0
        params["vote_count.gte"] = 100 # Чтобы не попадались фильмы с 1 оценкой
    elif extra == "short":
        params["with_runtime.lte"] = 90
    elif extra == "long":
        params["with_runtime.gte"] = 150

    # Делаем основной запрос
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json().get("results", [])[:5]
    else:
        print(f"Ошибка API: {response.status_code} - {response.text}")
        return []
