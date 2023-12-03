import json
from math import ceil

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.check_startswith import get_all_anime


async def anime_keyboard(anime_per_row: int = 2, page: int = 1,
                         offset: int = 6) -> InlineKeyboardMarkup:
    all_anime = get_all_anime()

    anime_list = [anime.get("title") for anime in all_anime]
    total_pages = ceil(len(anime_list) / offset)

    if page <= 0:
        page = total_pages
    if page > total_pages:
        page = 1

    start_index = (page - 1) * offset
    end_index = start_index + offset
    current_list = anime_list[start_index:end_index]

    anime_chunks = [current_list[i:i + anime_per_row] for i in range(0, len(current_list), anime_per_row)]
    markup = InlineKeyboardMarkup(row_width=anime_per_row + 1)

    markup.add(InlineKeyboardButton("Подписаться на все", callback_data='subscribe_all_anime'))
    for row in anime_chunks:
        buttons = [
            InlineKeyboardButton(
                text=f'{anime[0: 25]}...',
                callback_data=f'anime_{anime[0: 20]}')
            for i, anime in enumerate(row)
        ]
        markup.add(*buttons)

    pagination_buttons = [
        InlineKeyboardButton("<-", callback_data=f'prev_anime_page_{page}'),
        InlineKeyboardButton(f'{page}/{total_pages}', callback_data=f'page_anime_{page}'),
        InlineKeyboardButton("->", callback_data=f'next_anime_page_{page}')
    ]

    markup.add(*pagination_buttons)
    markup.add(InlineKeyboardButton("На главную", callback_data='back'))

    return markup
