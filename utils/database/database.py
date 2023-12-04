from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args):
        async with self.pool.acquire() as connection:
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
    id BIGINT PRIMARY KEY,
    username VARCHAR(50)
);
CREATE TABLE IF NOT EXISTS subscriptions (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    anime_title VARCHAR REFERENCES anime(title)
);
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'uc_user_anime'
          AND conrelid = 'subscriptions'::regclass
    ) THEN
        EXECUTE 'ALTER TABLE subscriptions ADD CONSTRAINT uc_user_anime UNIQUE (user_id, anime_title)';
    END IF;
END $$;
        '''
        await self.execute(sql)
