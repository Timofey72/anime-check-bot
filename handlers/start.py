from aiogram import Dispatcher, types

import messages
from utils.database.anime import Anime
from utils.database.user import User


async def create_user_if_not_exists(telegram_id, username):
    user = await User().select_user(id=telegram_id)
    if not user:
        await User().add_user(telegram_id=telegram_id, username=username)


async def start(message: types.Message):
    await create_user_if_not_exists(message.from_user.id, message.from_user.username)
    return await message.answer(messages.GREETING)


async def anime(message: types.Message):
    anime_all = await Anime().select_all_anime()
    msg = ''
    for index, item in enumerate(anime_all):
        msg += f'{index + 1}. {item.get("title")} - <a href="{item.get("link")}">смотреть</a>\n'
    return await message.answer(msg, parse_mode='HTML')


def register_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(anime, commands=['anime'])
