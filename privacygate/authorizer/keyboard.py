from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from . import callbackdata


subscription_dialog = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅Да",
                                 callback_data=callbackdata.SubscriptionRequests(answer="yes").pack()),
            InlineKeyboardButton(text="🚫Нет",
                                 callback_data=callbackdata.SubscriptionRequests(answer="no").pack())
        ]
    ]
)

