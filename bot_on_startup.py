import logging
import asyncio

from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data.config import bot, setup_databases, anime_db, ADMINS
from handlers import start
from scraper import get_all_anime
from scraper import get_new_episodes

dp = Dispatcher(bot, storage=MemoryStorage())


async def check_ongoing_anime(db):
    while True:
        all_anime = get_all_anime.main()
        await db.add_many_anime(all_anime)
        await asyncio.sleep(60)


async def check_new_episodes():
    while True:
        new_anime = get_new_episodes.main()
        message = ''
        for i, anime in enumerate(new_anime):
            message += (f'{i + 1}. Вышла {anime.episode} {anime.title}. '
                        f'<a href="https://animego.org/{anime.link}">Нажмите</a>, чтобы посмотреть\n')
        if not message:
            await bot.send_message(ADMINS[0], 'Список пуст.', parse_mode='HTML')
        else:
            await bot.send_message(ADMINS[0], message, parse_mode='HTML')
        await asyncio.sleep(60)


async def on_startup(dispatcher):
    start.register_start(dispatcher)

    logging.info('Database configure')
    await setup_databases()

    logging.info('Schedule starting...')
    asyncio.create_task(check_ongoing_anime(anime_db))
    asyncio.create_task(check_new_episodes())

    logging.info('Bot started')
