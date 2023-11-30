from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.poll: Union[Pool, None] = None

    async def create(self):
        self.poll = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args):
        await self.create()
        async with self.poll.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                result = await connection.execute(command, *args)
            return result

    async def create_tables(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS anime (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) UNIQUE,
            link VARCHAR(255),
            last_episode INTEGER
        );
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50)
        );
        CREATE TABLE IF NOT EXISTS subscriptions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            anime_title VARCHAR REFERENCES anime(title)
        );
        '''
        await self.execute(sql)
