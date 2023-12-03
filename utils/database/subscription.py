from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Subscription:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args, fetch: bool = False, fetchval: bool = False, fetchrow: bool = False,
                      execute: bool = False):
        async with self.pool.acquire() as connection:
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
    def format_args_for_insert(user_id: int, anime_title: list):
        sql = (', '.join(
            [f"((SELECT id FROM users WHERE id={user_id}), (SELECT title FROM anime WHERE title='{title}'))" for title
             in
             anime_title]) + ' ON CONFLICT (user_id, anime_title) DO NOTHING;')
        return sql

    @staticmethod
    def format_update(sql, parameters: dict):
        sql += ', '.join([
            f'{item} = ${num}' for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_subscription(self, user_id, anime_title):
        sql = '''
            INSERT INTO subscriptions (user_id, anime_title)
            VALUES (
                (SELECT id FROM users WHERE id=$1),
                (SELECT title FROM anime WHERE title=$2)
            )
            RETURNING *;
        '''
        return await self.execute(sql, user_id, anime_title, fetchrow=True)

    async def select_all_subscriptions(self, user_id):
        sql = f'SELECT * FROM subscriptions WHERE user_id = {user_id}'
        return await self.execute(sql, fetch=True)

    async def select_subscription(self, **kwargs):
        sql = 'SELECT * FROM subscriptions WHERE '
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def delete_subscription(self, **kwargs):
        sql = f'DELETE FROM subscriptions WHERE '
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def add_many_subscriptions(self, user_id: int, anime_title: list):
        sql = '''INSERT INTO subscriptions (user_id, anime_title) VALUES '''
        sql += self.format_args_for_insert(user_id, anime_title)
        return await self.execute(sql, fetchrow=True)

    async def count_subscriptions(self, user_id):
        sql = f'SELECT COUNT(*) FROM subscriptions WHERE user_id = {user_id}'
        return await self.execute(sql, fetchval=True)
