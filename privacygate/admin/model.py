from ..database import *


def check_admin(user_id: int) -> bool:
    user = get_user(user_id)
    return bool(user[0][4])


def add_admin(user_id: int):
    update_user(user_id, "admin", "1")


def remove_admin(user_id: int):
    update_user(user_id, "admin", "0")


def count_users() -> int:
    return len(all_subscription_request())


def count_requests() -> int:
    return len(all_users())


def get_users(num_first_key: int, count: int) -> tuple[list[tuple], bool]:
    flag_end = False
    users = all_users()
    num_stop_key = num_first_key + count

    if num_stop_key >= len(users):
        flag_end = True
        num_stop_key = len(users)

    select_users = [(users[i][0], users[i][1]) for i in range(num_first_key, num_stop_key)]

    return select_users, flag_end


def get_requests(num_first_key: int, count: int) -> tuple[list[tuple], bool]:
    flag_end = False
    users = all_subscription_request()
    num_stop_key = num_first_key + count

    if num_stop_key >= len(users):
        flag_end = True
        num_stop_key = len(users)

    select_users = [(users[i][0], users[i][1]) for i in range(num_first_key, num_stop_key)]

    return select_users, flag_end
