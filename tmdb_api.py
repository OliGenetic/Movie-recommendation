import requests
import config

BASE_URL = "https://api.themoviedb.org/3"

KEYWORDS = {
    "plot_games": "152368",   
    "plot_comics": "9715",    
    "plot_books": "818",      
    "char_robots": "11035",   
    "char_animals": "14760",  
    "char_aliens": "14909",   
    "char_vampires": "3133"   
}

def get_recommendations(state):
    media_type = "movie"
    if state.get('format') in ['tv', 'dorama', 'anime']:
        media_type = "tv"
    
    url = f"{BASE_URL}/discover/{media_type}"
    
    params = {
        "api_key": config.TMDB_API_KEY,
        "language": "ru-RU",
        "sort_by": "popularity.desc",
        "page": page
    }

    # 1. ФОРМАТ
    fmt = state.get('format')
    if fmt == 'cartoon':
        params["with_genres"] = "16"
    elif fmt == 'anime':
        params["with_genres"] = "16"
        params["with_keywords"] = "210024"
    elif fmt == 'dorama':
        params["with_origin_country"] = "KR"

    # 2. НАСТРОЕНИЕ
    mood = state.get('mood')
    mood_genres = []
    if mood == "relax": mood_genres = ["35", "10751"]
    elif mood == "thrill": mood_genres = ["28", "53", "27"]
    elif mood == "think": mood_genres = ["878", "9648", "18"]
    elif mood == "cry": mood_genres = ["18", "10749"]
    elif mood == "dream": mood_genres = ["14", "12"]
    elif mood == "laugh": mood_genres = ["35"]
    elif mood == "romance": mood_genres = ["10749"]
    
    if mood_genres:
        if "with_genres" in params: params["with_genres"] += "," + ",".join(mood_genres)
        else: params["with_genres"] = ",".join(mood_genres)

    # 3. ГОД
    year = state.get('year')
    if year != "any":
        start_year = int(year.split("_")[0])
        end_year = int(year.split("_")[1])
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

    # 5 и 6. ОСНОВА СЮЖЕТА И ПЕРСОНАЖИ
    keywords = []
    if state.get('plot') in KEYWORDS: keywords.append(KEYWORDS[state.get('plot')])
    if state.get('char') in KEYWORDS: keywords.append(KEYWORDS[state.get('char')])
    if keywords:
        params["with_keywords"] = ",".join(keywords)

    # 7. СТУДИЯ
    studio = state.get('studio')
    if studio != "any":
        params["with_companies"] = studio

    # 8. РЕЙТИНГ
    rating = state.get('rating')
    if rating == "7":
        params["vote_average.gte"] = 7.0
        params["vote_count.gte"] = 50
    elif rating == "8":
        params["vote_average.gte"] = 8.0
        params["vote_count.gte"] = 100

    # 9. ДЛИТЕЛЬНОСТЬ (работает только для фильмов)
    runtime = state.get('runtime')
    if media_type == "movie":
        if runtime == "short": params["with_runtime.lte"] = 90
        elif runtime == "medium":
            params["with_runtime.gte"] = 90
            params["with_runtime.lte"] = 150
        elif runtime == "long": params["with_runtime.gte"] = 150

    # Запрос к API
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])[:5] # Берем 5 фильмов с текущей страницы
        total_pages = data.get("total_pages", 1)
        return results, total_pages
    else:
        print(f"Ошибка API: {response.status_code} - {response.text}")
        return [], 0
