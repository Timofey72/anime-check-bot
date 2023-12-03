import bs4
import json
import requests

from typing import NamedTuple, List
from bs4 import BeautifulSoup

BASE_URL = 'https://animego.org/'


class AnimeData(NamedTuple):
    title: str
    link: str


def get_all_anime() -> list:
    page_count = 1
    anime = []

    while True:
        res = requests.get(BASE_URL + f'anime/filter/status-is-ongoing/apply?page={page_count}')
        if res.status_code == 404:
            break

        soup = BeautifulSoup(res.text, 'lxml')
        anime_list = soup.find('div', id='anime-list-container').find_all('div', class_='media-body')
        anime.extend(anime_list)

        page_count += 1

    return anime


def parse_anime_data(anime: bs4.element.Tag) -> AnimeData:
    title = anime.find('div', class_='h5 font-weight-normal mb-1').find('a').text
    link = anime.find('div', class_='h5 font-weight-normal mb-1').find('a').get('href')

    return AnimeData(title, link)


def main() -> List[AnimeData]:
    anime = get_all_anime()
    result = []
    json_result = {'data': []}
    for one_anime in anime:
        data = parse_anime_data(one_anime)
        result.append(data)
        json_result['data'].append({
            'title': data.title,
            'link': data.link
        })

    with open('scraper/anime_data.json', 'w', encoding='utf-8') as f:
        json.dump(json_result, f, indent=2, ensure_ascii=False)

    return result


if __name__ == '__main__':
    main()
