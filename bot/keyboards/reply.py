from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.constants import (
    USER_MENU_ACCOUNT,
    USER_MENU_COINS,
    USER_MENU_HELP,
    USER_MENU_REDEEM,
    USER_MENU_REFERRAL,
    USER_MENU_SEARCH,
)


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=USER_MENU_SEARCH),
                KeyboardButton(text=USER_MENU_ACCOUNT),
            ],
            [
                KeyboardButton(text=USER_MENU_COINS),
                KeyboardButton(text=USER_MENU_REFERRAL),
            ],
            [
                KeyboardButton(text=USER_MENU_REDEEM),
                KeyboardButton(text=USER_MENU_HELP),
            ],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )
