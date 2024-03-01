from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from . import callbackdata
from . import model


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🕺Участники"),
            KeyboardButton(text="🗂Заявки")
        ],
        [
            KeyboardButton(text="Выйти из админки")
        ]
    ],
    resize_keyboard=True
)


def list_users(num_page: int) -> InlineKeyboardMarkup:
    count_on_page = 3
    num_first_user = num_page * count_on_page
    users, flag_end = model.get_users(num_first_user, count_on_page)

    builder = InlineKeyboardBuilder()
    for user in users:
        builder.row(InlineKeyboardButton(text=user[1],
                                         callback_data=callbackdata.UserInfo(type_info="member",
                                                                             user_id=user[0],
                                                                             num_page=num_page).pack()))

    button_prev = InlineKeyboardButton(text="⬅️",
                                       callback_data=callbackdata.UsersList(type_list="members",
                                                                            num_page=num_page-1).pack())
    button_next = InlineKeyboardButton(text="➡️️",
                                       callback_data=callbackdata.UsersList(type_list="members",
                                                                            num_page=num_page+1).pack())
    if num_page and not flag_end:
        builder.row(button_prev, button_next)
    elif num_page:
        builder.row(button_prev)
    elif not flag_end:
        builder.row(button_next)

    builder.row(InlineKeyboardButton(text="Отмена",
                                     callback_data=callbackdata.UsersList(type_list="cancel",
                                                                          num_page=num_page).pack()))

    return builder.as_markup()


def edit_user(user_id: int, num_page: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Удалить",
                                     callback_data=callbackdata.DeleteUser(user_id=user_id,
                                                                           num_page=num_page).pack()),
                InlineKeyboardButton(text="Назад",
                                     callback_data=callbackdata.UsersList(type_list="members",
                                                                          num_page=num_page).pack())
            ]
        ]
    )
    return keyboard


def list_requests(num_page: int) -> InlineKeyboardMarkup:
    count_on_page = 3
    num_first_user = num_page * count_on_page
    users, flag_end = model.get_requests(num_first_user, count_on_page)

    builder = InlineKeyboardBuilder()
    for user in users:
        builder.row(InlineKeyboardButton(text=user[1],
                                         callback_data=callbackdata.UserInfo(type_info="request",
                                                                             user_id=user[0],
                                                                             num_page=num_page).pack()))

    button_prev = InlineKeyboardButton(text="⬅️",
                                       callback_data=callbackdata.UsersList(type_list="requests",
                                                                            num_page=num_page-1).pack())
    button_next = InlineKeyboardButton(text="➡️️",
                                       callback_data=callbackdata.UsersList(type_list="requests",
                                                                            num_page=num_page+1).pack())
    if num_page and not flag_end:
        builder.row(button_prev, button_next)
    elif num_page:
        builder.row(button_prev)
    elif not flag_end:
        builder.row(button_next)

    builder.row(InlineKeyboardButton(text="Отмена",
                                     callback_data=callbackdata.UsersList(type_list="cancel",
                                                                          num_page=num_page).pack()))

    return builder.as_markup()


def edit_request(user_id: int, num_page: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Принять",
                                     callback_data=callbackdata.ProcessingRequest(user_id=user_id,
                                                                                  action="accept",
                                                                                  num_page=num_page).pack()),
                InlineKeyboardButton(text="Отклонить",
                                     callback_data=callbackdata.ProcessingRequest(user_id=user_id,
                                                                                  action="reject",
                                                                                  num_page=num_page).pack())
            ],
            [
                InlineKeyboardButton(text="Назад",
                                     callback_data=callbackdata.UsersList(type_list="requests",
                                                                          num_page=num_page).pack())
            ]
        ]
    )
    return keyboard
