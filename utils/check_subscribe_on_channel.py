import logging

from aiogram.types import ChatMemberStatus

from data.config import bot, CHANNEL_ID


async def check_subscription(user_id: int) -> bool:
    try:
        chat_member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if chat_member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
            return True
    except Exception as ex:
        logging.error(f"Check Subscription error: {ex}")

    return False
