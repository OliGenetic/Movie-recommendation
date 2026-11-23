import requests
import config

BASE_URL = "https://api.themoviedb.org/3"

def get_movies(year, genre_id, mood, country, actor_name=None):
    url = f"{BASE_URL}/discover/movie"
    
    # Базовые параметры запроса
    params = {
        "api_key": config.TMDB_API_KEY,
        "language": "ru-RU",
        "sort_by": "popularity.desc",
        "page": 1
    }

    # 1. Обработка года
    if year and year != "any":
        if year.endswith("s"): # Обработка десятилетий (например, 2020s)
            start_year = int(year[:4])
            params["primary_release_date.gte"] = f"{start_year}-01-01"
            params["primary_release_date.lte"] = f"{start_year+9}-12-31"
        else:
            params["primary_release_year"] = year

    # 2. Обработка жанра и настроения
    genre_ids = []
    if genre_id and genre_id != "any":
        genre_ids.append(genre_id)
        
    # Добавляем жанры в зависимости от настроения
    if mood == "mood_relax":
        genre_ids.extend(["35", "10751"]) # Комедия, Семейный
    elif mood == "mood_thrill":
        genre_ids.extend(["53", "27"])    # Триллер, Ужасы
    elif mood == "mood_think":
        genre_ids.extend(["18", "9648"])  # Драма, Детектив
        
    if genre_ids:
        params["with_genres"] = ",".join(genre_ids)

    # 3. Обработка страны
    if country and country != "any":
        params["with_origin_country"] = country

    # 4. Поиск ID актера (если введен)
    if actor_name:
        search_url = f"{BASE_URL}/search/person"
        search_params = {"api_key": config.TMDB_API_KEY, "query": actor_name}
        res = requests.get(search_url, params=search_params).json()
        if res.get("results"):
            params["with_cast"] = res["results"][0]["id"] # Берем ID первого совпадения

    # Делаем основной запрос
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        # Возвращаем первые 5 фильмов
        return response.json().get("results", [])[:5]
    else:
        print(f"Ошибка API: {response.status_code} - {response.text}")
        return []
