import asyncio

import asyncpg

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data.config import bot, ADMINS, anime_db
from scraper import get_new_episodes
from scraper import get_all_anime


async def check_new_episodes():
    # TASK | IT'S TEST. NOT FINALIZED
    new_anime = get_new_episodes.main()
    message = ''
    for i, anime in enumerate(new_anime):
        message += (f'{i + 1}. Вышла {anime.episode} {anime.title}. '
                    f'<a href="https://animego.org/{anime.link}">Нажмите</a>, чтобы посмотреть\n\n')
    if not message:
        return await bot.send_message(ADMINS[0], 'Список пуст.', parse_mode='HTML')
    return await bot.send_message(ADMINS[0], message, parse_mode='HTML')


async def check_ongoing_anime():
    all_anime = get_all_anime.main()
    try:
        await anime_db.add_many_anime(all_anime)
    except asyncpg.exceptions.PostgresSyntaxError as ex:
        print(ex)


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_new_episodes, 'interval', hours=1)
    scheduler.add_job(check_ongoing_anime, 'interval', days=1)
    scheduler.start()

    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == '__main__':
    asyncio.run(check_new_episodes())
    asyncio.run(check_ongoing_anime())
    asyncio.run(main())
