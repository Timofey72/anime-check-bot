from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def subscription_keyboard(subscriptions: list, subscriptions_per_row: int, page: int = 0) -> InlineKeyboardMarkup:
    subscription_chunks = [subscriptions[i:i + subscriptions_per_row] for i in
                           range(0, len(subscriptions), subscriptions_per_row)]
    markup = InlineKeyboardMarkup(row_width=subscriptions_per_row + 1)

    markup.add(InlineKeyboardButton("Отменить все", callback_data='cancel_subscriptions'))
    for row in subscription_chunks:
        buttons = [InlineKeyboardButton(subscription, callback_data=f'subscription_{subscription}') for i, subscription
                   in
                   enumerate(row)]
        markup.add(*buttons)

    markup.add(*[
        InlineKeyboardButton("<-", callback_data='subscription_prev_page'),
        InlineKeyboardButton(str(page), callback_data=f'subscription_page_{page}'),
        InlineKeyboardButton("->", callback_data='subscription_next_page')
    ])
    markup.add(InlineKeyboardButton("На главную", callback_data='back'))

    return markup
