from aiogram import F, Router
from aiogram.types import Message

from bot.constants import USER_MENU_REFERRAL
from bot.data.texts import referral_text, user_not_found_text
from bot.handlers.start import ensure_access_or_prompt
from bot.keyboards.reply import main_menu_keyboard
from bot.services.referral_service import get_referral_summary

router = Router(name=__name__)


@router.message(F.text == USER_MENU_REFERRAL)
async def referral_handler(message: Message) -> None:
    if not await ensure_access_or_prompt(message):
        return

    tg_user = message.from_user
    if tg_user is None:
        return

    summary = get_referral_summary(tg_user.id)
    if summary is None:
        await message.answer(user_not_found_text())
        return

    await message.answer(
        referral_text(
            referral_link=summary["referral_link"],
            referral_count=summary["referral_count"],
            earned_coins=summary["earned_coins"],
        ),
        reply_markup=main_menu_keyboard(),
    )
