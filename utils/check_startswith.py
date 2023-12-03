import json
from typing import Optional


def check_startswith(data: str) -> Optional[dict]:
    with open('scraper/anime_data.json', 'r', encoding='utf-8') as f:
        all_anime = json.loads(f.read())['data']
        for anime_obj in all_anime:
            if anime_obj['title'].startswith(data):
                return anime_obj
    return None


def get_all_anime() -> list:
    with open('scraper/anime_data.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())['data']
