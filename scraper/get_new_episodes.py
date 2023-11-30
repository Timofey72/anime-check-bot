from typing import NamedTuple, List

import bs4
import requests

from bs4 import BeautifulSoup

BASE_URL = 'https://animego.org/'


class AnimeEpisodeData(NamedTuple):
    title: str
    episode: str
    link: str


def get_all_anime() -> BeautifulSoup:
    content = requests.get(BASE_URL).text
    soup = BeautifulSoup(content, 'lxml')
    anime_list = soup.find('div', class_='last-update-container')

    return anime_list


def parse_anime_data(anime: bs4.element.Tag) -> AnimeEpisodeData:
    title = anime.find('span', class_='last-update-title').text
    episode = anime.find('div', class_='font-weight-600 text-truncate').text
    link = anime.get('onclick').replace("location.href='/", '')[:-1] + '#video-watch2'

    return AnimeEpisodeData(title, episode, link)


def main() -> List[AnimeEpisodeData]:
    anime = get_all_anime()
    result = []

    for one_anime in anime:
        data = parse_anime_data(one_anime)
        if data not in result:
            result.append(data)

    return result


if __name__ == '__main__':
    main()
