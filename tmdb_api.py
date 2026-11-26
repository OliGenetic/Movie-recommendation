import requests
import config
import random

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

def get_recommendations(state, page=1):    
    # Защита от ошибки 400 (TMDB не отдает страницы выше 500)
    if page > 500:
        return [], 500

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
    if fmt == 'movie':
        # Исключаем мультфильмы (16) и аниме (210024) из обычных фильмов
        params["without_genres"] = "16"
        params["without_keywords"] = "210024"
    elif fmt == 'cartoon':
        params["with_genres"] = "16"
        params["without_keywords"] = "210024" # Исключаем аниме из мультфильмов
    elif fmt == 'anime':
        params["with_genres"] = "16"
        params["with_keywords"] = "210024"
    elif fmt == 'dorama':
        # Исключаем аниме из дорам
        params["without_genres"] = "16" 
        params["without_keywords"] = "210024"
    
        # Если страна не выбрана, ищем по всем азиатским странам
        if state.get('country') == "any":
            params["with_origin_country"] = "KR|JP|CN|TW"

    # 2. НАСТРОЕНИЕ
    mood = state.get('mood')
    mood_genres = []
    if mood == "relax": mood_genres = ["10751", "35", "10402", "10770"] # Family (10751), Comedy (35), Music (10402), TV Movie (10770)
    elif mood == "thrill": mood_genres = ["28", "53", "27"] # Action (28), Thriller (53), Horror (27)
    elif mood == "think": mood_genres = ["878", "9648", "80", "90"] # Mystery (878), Science Fiction (9648), Crime (80), Documentary (90)
    elif mood == "cry": mood_genres = ["18", "10752"] # Drama (18), War (10752)
    elif mood == "dream": mood_genres = ["14", "12"] # Fantasy (14), Adventure (12)
    elif mood == "laugh": mood_genres = ["35"] # Comedy (35)
    elif mood == "romance": mood_genres = ["10749"] # Romance (10749)
    
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
    if country != "any" and fmt not in ['anime']:
        # Если выбрана конкретная страна, применяем её
        params["with_origin_country"] = country

    # 5. ОСНОВА СЮЖЕТА
    keywords = []
    if state.get('plot') in KEYWORDS: keywords.append(KEYWORDS[state.get('plot')])

    # 6. ПЕРСОНАЖИ
    if state.get('char') in KEYWORDS: keywords.append(KEYWORDS[state.get('char')])
    if keywords:
        params["with_keywords"] = ",".join(keywords)

    # 7. РЕЙТИНГ
    rating = state.get('rating')
    if rating == "6":
        params["vote_average.gte"] = 6.0
        params["vote_count.gte"] = 20
    elif rating == "7":
        params["vote_average.gte"] = 7.0
        params["vote_count.gte"] = 50
    elif rating == "8":
        params["vote_average.gte"] = 8.0
        params["vote_count.gte"] = 100

    # 8. ДЛИТЕЛЬНОСТЬ (работает только для фильмов)
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
        results = data.get("results", [])[:5]
        total_pages = min(data.get("total_pages", 1), 500) # Ограничиваем 500 страницами
        return results, total_pages
    else:
        print(f"Ошибка API: {response.status_code} - {response.text}")
        return [], 0

# Случайный известный фильм
def get_random_movie():
    random_page = random.randint(1, 10) 
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": config.TMDB_API_KEY,
        "language": "ru-RU",
        "sort_by": "popularity.desc",
        "vote_average.gte": 6.5,
        "vote_count.gte": 100,
        "page": random_page
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            return random.choice(results)
    return None

# СЕЗОННЫЕ ФИЛЬМЫ
# Новогодние фильмы
def get_new_year_movies(page=1):    
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": config.TMDB_API_KEY,
        "language": "ru-RU",
        "sort_by": "popularity.desc",
        "with_keywords": "207317|613", # Ищем фильмы, связанные с Рождеством (207317) или кануном Нового года (613)
        "vote_average.gte": 6.0,
        "vote_count.gte": 50,
        "page": page
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])[:5]
            total_pages = min(data.get("total_pages", 1), 500)
            return results, total_pages
        return [], 0

    except requests.exceptions.RequestException:
        return [], 0

def get_english_overview(item_id, is_tv=False):
    endpoint = "tv" if is_tv else "movie"
    url = f"{BASE_URL}/{endpoint}/{item_id}"
    params = {
        "api_key": config.TMDB_API_KEY,
        "language": "en-US"  # В случае отсутствия описания на русском, запрашиваем английский язык
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('overview', '').strip()
    return ""
