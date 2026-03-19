from aiogram import F, Router
from aiogram.types import Message

from bot.constants import (
    USER_MENU_ACCOUNT,
    USER_MENU_COINS,
    USER_MENU_HELP,
)
from bot.data.texts import (
    account_text,
    coins_text,
    help_text,
    user_not_found_text,
)
from bot.handlers.start import ensure_access_or_prompt
from bot.keyboards.reply import main_menu_keyboard
from bot.services.user_service import (
    get_account_summary,
    get_user_coins,
)

router = Router(name=__name__)


@router.message(F.text == USER_MENU_ACCOUNT)
async def account_handler(message: Message) -> None:
    if not await ensure_access_or_prompt(message):
        return

    tg_user = message.from_user
    if tg_user is None:
        return

    summary = get_account_summary(tg_user.id)
    if summary is None:
        await message.answer(user_not_found_text())
        return

    await message.answer(
        account_text(
            user_id=summary["telegram_id"],
            full_name=summary["full_name"],
            username=summary["username"],
            coins=summary["coins"],
            total_searches=summary["total_searches"],
            referral_count=summary["referral_count"],
            joined_at=summary["joined_at"],
            referral_link=summary["referral_link"],
        ),
        reply_markup=main_menu_keyboard(),
    )


@router.message(F.text == USER_MENU_COINS)
async def coins_handler(message: Message) -> None:
    if not await ensure_access_or_prompt(message):
        return

    tg_user = message.from_user
    if tg_user is None:
        return

    coins = get_user_coins(tg_user.id)
    if coins is None:
        await message.answer(user_not_found_text())
        return

    await message.answer(
        coins_text(coins=coins),
        reply_markup=main_menu_keyboard(),
    )


@router.message(F.text == USER_MENU_HELP)
async def help_handler(message: Message) -> None:
    if not await ensure_access_or_prompt(message):
        return

    await message.answer(
        help_text(),
        reply_markup=main_menu_keyboard(),
    )
