from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.constants import USER_MENU_REDEEM
from bot.data.texts import (
    promo_already_used_text,
    promo_expired_text,
    promo_inactive_text,
    promo_invalid_text,
    promo_limit_reached_text,
    promo_redeem_error_text,
    redeem_cancelled_text,
    redeem_prompt_text,
    redeem_success_text,
    user_not_found_text,
)
from bot.handlers.start import ensure_access_or_prompt
from bot.keyboards.reply import main_menu_keyboard
from bot.services.promo_service import redeem_promo_code
from bot.services.user_service import get_user
from bot.states import PromoStates

router = Router(name=__name__)


@router.message(F.text == USER_MENU_REDEEM)
async def redeem_menu_handler(message: Message, state: FSMContext) -> None:
    if not await ensure_access_or_prompt(message):
        return

    tg_user = message.from_user
    if tg_user is None:
        return

    user = get_user(tg_user.id)
    if user is None:
        await message.answer(user_not_found_text())
        return

    await state.set_state(PromoStates.waiting_for_code)
    await message.answer(
        redeem_prompt_text(),
        reply_markup=main_menu_keyboard(),
    )


@router.message(PromoStates.waiting_for_code, F.text.casefold() == "cancel")
async def redeem_cancel_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        redeem_cancelled_text(),
        reply_markup=main_menu_keyboard(),
    )


@router.message(PromoStates.waiting_for_code)
async def redeem_code_handler(message: Message, state: FSMContext) -> None:
    if not await ensure_access_or_prompt(message):
        return

    tg_user = message.from_user
    if tg_user is None or not message.text:
        return

    user = get_user(tg_user.id)
    if user is None:
        await state.clear()
        await message.answer(
            user_not_found_text(),
            reply_markup=main_menu_keyboard(),
        )
        return

    result = redeem_promo_code(
        telegram_id=tg_user.id,
        raw_code=message.text,
    )

    await state.clear()

    status = result["status"]

    if status == "success":
        await message.answer(
            redeem_success_text(
                code=result["code"],
                coins_added=result["coins_added"],
                new_balance=result["new_balance"],
            ),
            reply_markup=main_menu_keyboard(),
        )
        return

    if status == "invalid":
        await message.answer(
            promo_invalid_text(),
            reply_markup=main_menu_keyboard(),
        )
        return

    if status == "inactive":
        await message.answer(
            promo_inactive_text(),
            reply_markup=main_menu_keyboard(),
        )
        return

    if status == "expired":
        await message.answer(
            promo_expired_text(),
            reply_markup=main_menu_keyboard(),
        )
        return

    if status == "limit_reached":
        await message.answer(
            promo_limit_reached_text(),
            reply_markup=main_menu_keyboard(),
        )
        return

    if status == "already_used":
        await message.answer(
            promo_already_used_text(),
            reply_markup=main_menu_keyboard(),
        )
        return

    await message.answer(
        promo_redeem_error_text(),
        reply_markup=main_menu_keyboard(),
    )
