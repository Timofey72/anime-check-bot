import logging

from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data.config import bot, db
from handlers import start

dp = Dispatcher(bot, storage=MemoryStorage())


async def on_startup(dispatcher):
    start.register_start(dispatcher)

    logging.info('Database configure')
    await db.create()
    await db.create_tables()

    logging.info('Bot started')
