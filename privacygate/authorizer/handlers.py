from aiogram import Router
from aiogram.types import Message, CallbackQuery

from . import keyboard
from . import model
from . import callbackdata

router = Router()


def check_user_from_message(func):
    async def wrapper(*args, **kwargs) -> None:
        message: Message = args[0]
        if model.check_user(message.from_user.id):
            await func(*args)
        else:
            # TODO: удалить клавиатуру у пользователя
            await message.answer(f"Вы не в совете джедаев 🚷️. Подать заявку?",
                                 reply_markup=keyboard.subscription_dialog)
    return wrapper


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
