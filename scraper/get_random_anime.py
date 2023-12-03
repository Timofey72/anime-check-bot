from typing import NamedTuple

import bs4
import requests

from bs4 import BeautifulSoup

BASE_URL = 'https://animego.org/'


class AnimeEpisodeData(NamedTuple):
    title: str
    rating: str
    link: str
    image_url: str


def get_random_anime() -> (BeautifulSoup, str):
    response = requests.get(BASE_URL + 'anime/random')
    if response.status_code == 404:
        return get_random_anime()

    soup = BeautifulSoup(response.text, 'lxml')
    random_anime = soup.find('div', class_='media mb-3 d-none d-block d-md-flex')

    return random_anime, response.url


def parse_anime_data(anime: bs4.element.Tag, link: str) -> AnimeEpisodeData:
    title = anime.find('h1').text
    rating = anime.find('span', class_='rating-value').text
    image_url = anime.find('div', class_='anime-poster').find('img').get('src')

    return AnimeEpisodeData(title, rating, link, image_url)


def main() -> AnimeEpisodeData:
    return parse_anime_data(*get_random_anime())


if __name__ == '__main__':
    main()
