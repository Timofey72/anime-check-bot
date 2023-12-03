from typing import Union

from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import messages
from data.config import bot, user_db, subscriptions_db
from keyboards.anime_keyboard import anime_keyboard
from keyboards.main_keyboard import main_markup
from keyboards.subscription_keyboard import subscription_keyboard
from utils.check_startswith import check_startswith, get_all_anime


async def create_user_if_not_exists(telegram_id, username):
    user = await user_db.select_user(id=telegram_id)
    if not user:
        await user_db.add_user(telegram_id=telegram_id, username=username)


async def start(message: Union[types.Message, types.CallbackQuery]):
    await create_user_if_not_exists(message.from_user.id, message.from_user.username)
    if type(message) == types.CallbackQuery:
        message = message.message
        return await bot.edit_message_text(messages.GREETING, message.chat.id, message.message_id,
                                           reply_markup=main_markup)

    await message.answer(messages.GREETING, reply_markup=main_markup)


async def process_callback(callback_query: types.CallbackQuery):
    button_data = callback_query.data
    chat_id = callback_query.message.chat.id

    if button_data == 'my_subscriptions':
        await show_subscriptions(callback_query)
    elif button_data == 'anime_list':
        await show_anime_list(chat_id, callback_query.message.message_id)
    elif button_data == 'what_to_watch':
        await bot.edit_message_text('Посмотрите аниме', chat_id, callback_query.message.message_id)


async def show_subscriptions(callback_query: types.CallbackQuery, page=1):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    user_id = callback_query.from_user.id

    subscriptions = await subscriptions_db.select_all_subscriptions(user_id=user_id)
    if not subscriptions:
        return await bot.edit_message_text('У вас нет еще не одной активной подписки.', chat_id, message_id)
    markup = await subscription_keyboard(subscriptions, user_id=user_id, page=page)
    await bot.edit_message_text('Ваши активные подписки:', chat_id, message_id, reply_markup=markup)


async def process_subscription(callback_query: types.CallbackQuery):
    subscription_name = callback_query.data.replace('subscription_', '')
    chat_id = callback_query.message.chat.id

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('На главную', callback_data='back'))
    markup.add(InlineKeyboardButton('Отменить подписку', callback_data=f'unsubscribe_{subscription_name}'))
    if callback_query.data == 'subscription_all':
        return await bot.edit_message_text(f'Выбраны все аниме, вы уверены, что хотите их отменить?', chat_id,
                                           callback_query.message.message_id,
                                           reply_markup=markup)
    anime_title = check_startswith(subscription_name).get('title')
    await bot.edit_message_text(f'Выбрана подписка аниме: {anime_title}', chat_id, callback_query.message.message_id,
                                reply_markup=markup)


async def process_unsubscribe(callback_query: types.CallbackQuery):
    data = callback_query.data
    chat_id = callback_query.message.chat.id

    if data == 'unsubscribe_all':
        await subscriptions_db.delete_subscription(user_id=callback_query.from_user.id)
        message = 'Вы успешно отписались от всех аниме.'
        return await bot.edit_message_text(message, chat_id, callback_query.message.message_id)

    subscription_name = data.replace('unsubscribe_', '')
    anime_title = check_startswith(subscription_name).get('title')
    await subscriptions_db.delete_subscription(anime_title=anime_title, user_id=callback_query.from_user.id)
    message = 'Подписка отменена. Вам больше не будут приходить уведомления.'
    await bot.edit_message_text(message, chat_id, callback_query.message.message_id)


async def show_anime_list(chat_id, message_id, page=1):
    markup = await anime_keyboard(page=page)
    await bot.edit_message_text('Список всех аниме, которые сейчас выходят:', chat_id, message_id, reply_markup=markup)


async def show_anime(callback_query: types.CallbackQuery):
    data = callback_query.data.replace('anime_', '')
    anime = check_startswith(data)

    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("Подписаться", callback_data=f'subscribe_{data}'))
    markup.add(InlineKeyboardButton("На главную", callback_data='back'))

    message = (f'<b>{anime.get("title")}</b>\n\n'
               f'Подпишитесь, чтобы первыми узнавать о новых сериях!\n\n'
               f'<a href="{anime.get("link")}">Нажмите, чтобы посмотреть аниме.</a>')

    await bot.edit_message_text(message, callback_query.message.chat.id, callback_query.message.message_id,
                                reply_markup=markup, parse_mode='HTML')


async def process_subscribe(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id

    if callback_query.data == 'subscribe_all_anime':
        all_anime = get_all_anime()
        anime_titles = [anime.get('title') for anime in all_anime]
        await subscriptions_db.add_many_subscriptions(callback_query.from_user.id, anime_titles)
        return await bot.edit_message_text('Вы успешно подписались на все аниме!', chat_id, message_id)

    data = callback_query.data.replace('subscribe_', '')
    anime = check_startswith(data).get('title')
    await subscriptions_db.add_many_subscriptions(callback_query.from_user.id, [anime])

    message = 'Успешно! Теперь Вам будут приходить уведомления при выходе новых серий.'
    return await bot.edit_message_text(message, chat_id, message_id)


async def anime_pagination_next_page(callback_query: types.CallbackQuery):
    page = int(callback_query.data.replace('next_anime_page_', ''))
    await show_anime_list(callback_query.message.chat.id, callback_query.message.message_id, page + 1)


async def anime_pagination_prev_page(callback_query: types.CallbackQuery):
    page = int(callback_query.data.replace('prev_anime_page_', ''))
    await show_anime_list(callback_query.message.chat.id, callback_query.message.message_id, page - 1)


async def subs_pagination_next_page(callback_query: types.CallbackQuery):
    page = int(callback_query.data.replace('next_subs_page_', ''))
    await show_subscriptions(callback_query, page + 1)


async def subs_pagination_prev_page(callback_query: types.CallbackQuery):
    page = int(callback_query.data.replace('prev_subs_page_', ''))
    await show_subscriptions(callback_query, page - 1)


async def process_back(callback_query: types.CallbackQuery):
    return await start(callback_query)


def register_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_callback_query_handler(process_callback,
                                       lambda c: c.data in ['my_subscriptions', 'anime_list', 'what_to_watch'])
    dp.register_callback_query_handler(process_subscription,
                                       lambda c: c.data.startswith('subscription_'))
    dp.register_callback_query_handler(show_anime,
                                       lambda c: c.data.startswith('anime_'))
    dp.register_callback_query_handler(process_unsubscribe,
                                       lambda c: c.data.startswith('unsubscribe_'))
    dp.register_callback_query_handler(process_subscribe,
                                       lambda c: c.data.startswith('subscribe_'))
    dp.register_callback_query_handler(anime_pagination_next_page,
                                       lambda c: c.data.startswith('next_anime_page_'))
    dp.register_callback_query_handler(anime_pagination_prev_page,
                                       lambda c: c.data.startswith('prev_anime_page_'))
    dp.register_callback_query_handler(subs_pagination_next_page,
                                       lambda c: c.data.startswith('next_subs_page_'))
    dp.register_callback_query_handler(subs_pagination_prev_page,
                                       lambda c: c.data.startswith('prev_subs_page_'))
    dp.register_callback_query_handler(process_back,
                                       lambda c: c.data == 'back')
