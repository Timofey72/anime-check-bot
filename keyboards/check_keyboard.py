from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_check_keyboard(invite_link):
    markup = InlineKeyboardMarkup()
    markup.insert(InlineKeyboardButton(text='Подписаться на канал', url=invite_link))
    return markup
