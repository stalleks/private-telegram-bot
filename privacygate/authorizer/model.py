from ..database import *


def check_user(user_id: int) -> bool:
    contains = user_id in users
    return contains


def accept_user_request(user_id: int) -> bool:
    contains = user_id in subscription_requests
    if not contains:
        subscription_requests[user_id] = {"time": "21:00"}
    return contains
