from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_markup = InlineKeyboardMarkup(row_width=1)
buttons = [
    InlineKeyboardButton("Мои подписки", callback_data='my_subscriptions'),
    InlineKeyboardButton("Список аниме", callback_data='anime_list'),
    InlineKeyboardButton("Что посмотреть", callback_data='what_to_watch'),
]
main_markup.add(*buttons)
