from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants import VERIFY_FORCE_JOIN_CALLBACK


def force_join_keyboard(links: list[dict]) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    current_row: list[InlineKeyboardButton] = []

    for link in links:
        current_row.append(
            InlineKeyboardButton(
                text=link["title"],
                url=link["url"],
            )
        )
        if len(current_row) == 2:
            rows.append(current_row)
            current_row = []

    if current_row:
        rows.append(current_row)

    rows.append(
        [
            InlineKeyboardButton(
                text="✅ Verify",
                callback_data=VERIFY_FORCE_JOIN_CALLBACK,
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=rows)
