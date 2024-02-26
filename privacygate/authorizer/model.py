from ..database import *


def check_user(user_id: int) -> bool:
    check = bool(get_user(user_id))
    return check


def check_subscription_request(user_id: int) -> bool:
    check = bool(get_subscription_request(user_id))
    return check


def update_time_request(user_id: int):
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_subscription_request(user_id, "date_time", date_time)

