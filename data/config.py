import asyncio
import os

from aiogram import Bot
from dotenv import load_dotenv

from utils.database.anime import Anime
from utils.database.database import Database
from utils.database.subscription import Subscription
from utils.database.user import User

load_dotenv()

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))
MODE = str(os.getenv('MODE'))  # development or production
ADMINS = str(os.getenv('ADMINS')).split(',')

DB_USER = str(os.getenv('DB_USER'))
DB_PASSWORD = str(os.getenv('DB_PASSWORD'))
DB_HOST = str(os.getenv('DB_HOST'))
DB_NAME = str(os.getenv('DB_NAME'))

db = Database()
user_db = User()
subscriptions_db = Subscription()
anime_db = Anime()

loop = asyncio.get_event_loop()
loop.run_until_complete(user_db.create())
loop.run_until_complete(subscriptions_db.create())
loop.run_until_complete(anime_db.create())

bot = Bot(token=BOT_TOKEN)
