from typing import Union, List

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config
from scraper.get_all_anime import AnimeData


class Anime:
    def __init__(self):
        self.poll: Union[Pool, None] = None

    async def create(self):
        self.poll = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args, fetch: bool = False, fetchval: bool = False, fetchrow: bool = False,
                      execute: bool = False):
        await self.create()
        async with self.poll.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += ' AND '.join([
            f'{item} = ${num}' for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    @staticmethod
    def format_args_for_insert(parameters: List[AnimeData]):
        sql = (', '.join([f"('{item.title}', '{item.link}')" for item in parameters]) +
               ' ON CONFLICT (title) DO NOTHING;')
        return sql

    @staticmethod
    def format_update(sql, parameters: dict):
        sql += ', '.join([
            f'{item} = ${num}' for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_anime(self, title, link, last_episode=None):
        sql = 'INSERT INTO anime (title, link, last_episode) VALUES($1, $2, $3) returning *'
        return await self.execute(sql, title, link, last_episode, fetchrow=True)

    async def update_anime(self, title, **kwargs):
        sql = 'UPDATE anime SET '
        sql, parameters = self.format_update(sql, parameters=kwargs)
        sql += f' WHERE title={title}'
        return await self.execute(sql, *parameters, execute=True)

    async def select_all_anime(self):
        sql = 'SELECT * FROM anime'
        return await self.execute(sql, fetch=True)

    async def select_anime(self, **kwargs):
        sql = 'SELECT * FROM anime WHERE '
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def add_many_anime(self, args):
        sql = '''INSERT INTO anime (title, link) VALUES '''
        sql += self.format_args_for_insert(args)
        return await self.execute(sql, fetchrow=True)

    async def count_anime(self):
        sql = 'SELECT COUNT(*) FROM anime'
        return await self.execute(sql, fetchval=True)
