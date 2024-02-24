from aiogram import Router
from aiogram.types import Message, CallbackQuery

from . import keyboard
from . import model
from . import callbackdata

router = Router()


async def check_user(message: Message) -> bool:
    user_id = message.from_user.id
    contains = model.check_user(user_id)
    if not contains:
        # TODO: удалить клавиатуру у пользователя
        await message.answer(f"Вы не в совете джедаев 🚷️. Подать заявку?",
                             reply_markup=keyboard.subscription_dialog())
    return contains


@router.callback_query(callbackdata.SubscriptionRequests.filter(None))
async def accept_user_request(query: CallbackQuery, callback_data: callbackdata.SubscriptionRequests):
    if callback_data.answer == "yes":
        if model.accept_user_request(query.from_user.id):
            await query.answer("Вы уже подали заявку", show_alert=True)
            await query.message.delete()
        else:
            await query.message.edit_text("Заявка принята")
    else:
        await query.message.delete()
