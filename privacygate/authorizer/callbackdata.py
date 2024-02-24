from aiogram.filters.callback_data import CallbackData


class SubscriptionRequests(CallbackData, prefix="subscription"):
    answer: str