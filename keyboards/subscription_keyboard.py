from math import ceil
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import subscriptions_db


async def   subscription_keyboard(subscriptions: list, subscriptions_per_row: int = 2, page: int = 1,
                                offset: int = 6) -> InlineKeyboardMarkup:
    subscriptions_list = [sub.get('anime_title') for sub in subscriptions]
    total_pages = ceil(len(subscriptions_list) / offset)

    if page <= 0:
        page = total_pages
    if page > total_pages:
        page = 1

    start_index = (page - 1) * offset
    end_index = start_index + offset
    current_list = subscriptions_list[start_index:end_index]

    subscriptions_chunks = [current_list[i:i + subscriptions_per_row] for i in
                            range(0, len(current_list), subscriptions_per_row)]
    markup = InlineKeyboardMarkup(row_width=subscriptions_per_row + 1)

    markup.add(InlineKeyboardButton("Отписаться от всего", callback_data='subscription_all'))
    for row in subscriptions_chunks:
        buttons = [
            InlineKeyboardButton(
                text=f'{sub[0: 25]}...',
                callback_data=f'subscription_{sub[0: 20]}')
            for i, sub in enumerate(row)
        ]
        markup.add(*buttons)

    pagination_buttons = [
        InlineKeyboardButton(f'{page}/{total_pages}', callback_data=f'page_subs_{page}'),
    ]

    if total_pages > 1:
        pagination_buttons.insert(0, InlineKeyboardButton("<-", callback_data=f'prev_subs_page_{page}'))
        pagination_buttons.append(InlineKeyboardButton("->", callback_data=f'next_subs_page_{page}'))

    markup.add(*pagination_buttons)
    markup.add(InlineKeyboardButton("На главную", callback_data='back'))

    return markup
