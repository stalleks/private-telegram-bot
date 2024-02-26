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


manage_access = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Все участники",
                                 callback_data=callbackdata.UsersList(type_list="members", num_page=0).pack())
        ],
        [
            InlineKeyboardButton(text="Посмотреть заявки",
                                 callback_data=callbackdata.UsersList(type_list="requests", num_page=0).pack())
        ]
    ]
)


def list_members(num_page: int, count: int) -> InlineKeyboardMarkup:
    num_first_user = num_page * count
    users, flag_end = model.get_users(num_first_user, count)

    builder = InlineKeyboardBuilder()
    for key in users:
        builder.row(InlineKeyboardButton(text=users[key]["name"],
                                         callback_data=callbackdata.UserInfo(type_info="members",
                                                                             user_id=key).pack()))

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
