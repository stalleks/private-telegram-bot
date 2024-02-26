from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from . import model, callbackdata
from . import keyboard

router = Router()


class StatesUser(StatesGroup):
    admin = State()


def check_admin_from_message(func):
    async def wrapper(*args, **kwargs) -> None:
        message: Message = args[0]
        if model.check_admin(message.from_user.id):
            # TODO: передовать только актуальные аргументы
            await func(*args, kwargs["state"])
        else:
            # TODO: удалить клавиатуру у пользователя
            await message.answer("Вы не админ 🚷!")
    return wrapper


@router.message(Command("admin"))
@check_admin_from_message
async def command_admin_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(StatesUser.admin)
    await message.answer("Добро пожаловать в админку, Магистр", reply_markup=keyboard.menu)


@router.message(StatesUser.admin)
async def echo_handler(message: Message, state: FSMContext) -> None:
    if message.text == "Хочу стать админом":
        model.add_admin(message.from_user.id)
        await message.answer("Теперь вы админ")
    elif message.text == "Не хочу быть админом":
        model.remove_admin(message.from_user.id)
        await message.answer("Вы больше не админ")

    if message.text == keyboard.menu.keyboard[0][0].text:
        await message.answer("Управляйте доступом", reply_markup=keyboard.manage_access)
    elif message.text == keyboard.menu.keyboard[0][1].text:
        await message.answer("Обрабатывайте заявки")
    elif message.text == keyboard.menu.keyboard[1][0].text:
        await state.clear()
        await message.answer("Вы вышли из админки", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Неизвестная команда")


@router.callback_query(callbackdata.UsersList.filter(None))
async def manage_access(query: CallbackQuery, callback_data: callbackdata.UsersList):
    count_users = 3
    if callback_data.type_list == "members":
        await query.message.edit_text(f"Всего участников: {model.count_user()}. "
                                      f"\nВыберете участника",
                                      reply_markup=keyboard.list_members(callback_data.num_page, count_users))

    elif callback_data.type_list == "cancel":
        await query.message.delete()
