from aiogram import Dispatcher, types


async def start(message: types.Message):
    await message.answer('Hello')


def register_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
