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
        await message.answer(f"Всего участников: {model.count_users()}. "
                             f"\nВыберете участника",
                             reply_markup=keyboard.list_users(0))
    elif message.text == keyboard.menu.keyboard[0][1].text:
        await message.answer(f"Всего заявок: {model.count_requests()}. "
                             f"\nВыберете заявку",
                             reply_markup=keyboard.list_requests(0))
    elif message.text == keyboard.menu.keyboard[1][0].text:
        await state.clear()
        await message.answer("Вы вышли из админки", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Неизвестная команда")


@router.callback_query(callbackdata.UsersList.filter(None))
async def manage_access(query: CallbackQuery, callback_data: callbackdata.UsersList):
    if callback_data.type_list == "members":
        await query.message.edit_reply_markup(reply_markup=keyboard.list_users(callback_data.num_page))
    elif callback_data.type_list == "requests":
        await query.message.edit_reply_markup(reply_markup=keyboard.list_requests(callback_data.num_page))
    elif callback_data.type_list == "cancel":
        await query.message.delete()


@router.callback_query(callbackdata.UserInfo.filter(None))
async def show_user_info(query: CallbackQuery, callback_data: callbackdata.UserInfo):
    if callback_data.type_info == "member":
        user_info = model.get_user_info(callback_data.user_id)
        await query.message.edit_text(user_info, reply_markup=keyboard.edit_user(callback_data.user_id,
                                                                                 callback_data.num_page))
    elif callback_data.type_info == "request":
        request_info = model.get_request_info(callback_data.user_id)
        await query.message.edit_text(request_info, reply_markup=keyboard.edit_request(callback_data.user_id,
                                                                                       callback_data.num_page))


@router.callback_query(callbackdata.DeleteUser.filter(None))
async def delete_user(query: CallbackQuery, callback_data: callbackdata.DeleteUser):
    user_name = model.get_user_name(callback_data.user_id)
    model.remove_user(callback_data.user_id)
    await query.message.edit_text(f"Пользователь {user_name} удален!",
                                  reply_markup=keyboard.list_users(callback_data.num_page))


@router.callback_query(callbackdata.ProcessingRequest.filter(None))
async def show_request_info(query: CallbackQuery, callback_data: callbackdata.ProcessingRequest):
    if callback_data.action == "accept":
        user_name = model.accept_request(callback_data.user_id)
        await query.message.edit_text(f"Пользователь {user_name} добавлен!",
                                      reply_markup=keyboard.list_requests(callback_data.num_page))
    elif callback_data.action == "reject":
        user_name = model.reject_request(callback_data.user_id)
        await query.message.edit_text(f"Заявка пользователя {user_name} отклонена!",
                                      reply_markup=keyboard.list_requests(callback_data.num_page))
