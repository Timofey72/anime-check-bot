import logging
import asyncio
import re

from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import messages
from data.config import bot, setup_databases, anime_db, subscriptions_db, ADMINS
from handlers import start
from scraper import get_all_anime
from scraper import get_new_episodes

dp = Dispatcher(bot, storage=MemoryStorage())


async def check_ongoing_anime(db):
    while True:
        all_anime = get_all_anime.main()
        await db.add_many_anime(all_anime)
        await asyncio.sleep(60)


async def check_new_episodes(anime_database, subs_database):
    while True:
        new_anime = get_new_episodes.main()
        for i, anime in enumerate(new_anime):
            episode = int(re.findall(r'\d+', anime.episode)[0])
            anime_title = anime.title
            find_anime = await anime_database.select_anime(title=anime.title)

            if find_anime:
                send_message: bool = False

                if find_anime.get('last_episode') is None:
                    await anime_database.update_anime(title=anime.title, last_episode=episode)
                    send_message = True
                elif find_anime.get('last_episode') != episode:
                    send_message = True

                if send_message:
                    all_subscriptions = await subs_database.select_subscription(anime_title=anime_title)
                    for sub in all_subscriptions:
                        user_id = sub.get('user_id')
                        message = messages.NEW_EPISODE % (episode, anime_title, anime.link)
                        await bot.send_message(user_id, message, parse_mode='HTML')

            await asyncio.sleep(5)
        await asyncio.sleep(60)


async def on_startup(dispatcher):
    start.register_start(dispatcher)

    logging.info('Database configure')
    await setup_databases()

    logging.info('Schedule starting...')
    asyncio.create_task(check_ongoing_anime(anime_db))
    asyncio.create_task(check_new_episodes(anime_db, subscriptions_db))

    logging.info('Bot started')
