from ..database import *


def check_admin(user_id: int) -> bool:
    admin = users[user_id]["admin"]
    return admin


def add_admin(user_id: int):
    users[user_id]["admin"] = True


def remove_admin(user_id: int):
    users[user_id]["admin"] = False


def count_user() -> int:
    return len(users.keys())


def get_users(num_first_key: int, count: int) -> tuple[dict, bool]:
    flag_end = False
    num_stop_key = num_first_key + count
    keys = sorted(users.keys())
    if num_stop_key >= len(keys):
        flag_end = True
        num_stop_key = len(keys)

    select_users = {}
    for ind in range(num_first_key, num_stop_key):
        select_users[keys[ind]] = users[keys[ind]]

    return select_users, flag_end
