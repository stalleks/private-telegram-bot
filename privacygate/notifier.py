from aiogram import Bot
from .database import all_admin

bot: Bot = None


async def notify_all_admins(text: str, replay_markup) -> None:
    admins = all_admin()
    for admin in admins:
        await bot.send_message(chat_id=admin[0], text=text, reply_markup=replay_markup)