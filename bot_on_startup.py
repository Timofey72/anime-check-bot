import logging

from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data.config import bot
from handlers import start
from utils.database.database import Database

dp = Dispatcher(bot, storage=MemoryStorage())


async def on_startup(dispatcher):
    start.register_start(dispatcher)

    logging.info('Database configure')
    await Database().create_tables()

    logging.info('Bot started')
