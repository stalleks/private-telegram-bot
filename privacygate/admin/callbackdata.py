from aiogram.filters.callback_data import CallbackData


class UsersList(CallbackData, prefix="userslist"):
    type_list: str
    num_page: int


class DeleteUser(CallbackData, prefix="deleteuser"):
    user_id: int
    num_page: int


class UserInfo(CallbackData, prefix="userinfo"):
    type_info: str
    user_id: int
    num_page: int

