from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.constants import USER_MENU_SEARCH
from bot.data.texts import (
    insufficient_coins_text,
    no_results_text,
    search_cancelled_text,
    search_error_text,
    search_invalid_cnic_text,
    search_invalid_input_text,
    search_invalid_mobile_text,
    search_invalid_mobile_zero_text,
    search_not_configured_text,
    search_processing_text,
    search_prompt_text,
    user_not_found_text,
)
from bot.handlers.start import ensure_access_or_prompt
from bot.keyboards.reply import main_menu_keyboard
from bot.services.search_service import process_search
from bot.services.settings_service import get_search_cost_coins
from bot.services.user_service import get_user
from bot.states import SearchStates

router = Router(name=__name__)


@router.message(F.text == USER_MENU_SEARCH)
async def search_menu_handler(message: Message, state: FSMContext) -> None:
    if not await ensure_access_or_prompt(message):
        return

    tg_user = message.from_user
    if tg_user is None:
        return

    user = get_user(tg_user.id)
    if user is None:
        await message.answer(user_not_found_text())
        return

    await state.set_state(SearchStates.waiting_for_query)
    await message.answer(
        search_prompt_text(search_cost=get_search_cost_coins()),
        reply_markup=main_menu_keyboard(),
    )


@router.message(SearchStates.waiting_for_query, F.text.casefold() == "cancel")
async def cancel_search_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        search_cancelled_text(),
        reply_markup=main_menu_keyboard(),
    )


@router.message(SearchStates.waiting_for_query)
async def receive_search_query_handler(message: Message, state: FSMContext) -> None:
    if not await ensure_access_or_prompt(message):
        return

    tg_user = message.from_user
    if tg_user is None or not message.text:
        return

    await message.answer(search_processing_text())

    result = await process_search(
        telegram_id=tg_user.id,
        raw_query=message.text,
    )

    if not result["success"] and result.get("validation_only"):
        query_type = result["query_type"]

        if query_type == "mobile_with_zero":
            await message.answer(
                search_invalid_mobile_zero_text(),
                reply_markup=main_menu_keyboard(),
            )
        elif query_type == "invalid_cnic":
            await message.answer(
                search_invalid_cnic_text(),
                reply_markup=main_menu_keyboard(),
            )
        elif message.text.replace(" ", "").isdigit():
            await message.answer(
                search_invalid_mobile_text(),
                reply_markup=main_menu_keyboard(),
            )
        else:
            await message.answer(
                search_invalid_input_text(),
                reply_markup=main_menu_keyboard(),
            )
        return

    if not result["success"] and result.get("user_found") is False:
        await state.clear()
        await message.answer(
            user_not_found_text(),
            reply_markup=main_menu_keyboard(),
        )
        return

    if not result["success"] and result.get("insufficient_coins"):
        await state.clear()
        await message.answer(
            insufficient_coins_text(
                current_coins=result["current_coins"],
                required_coins=result["required_coins"],
            ),
            reply_markup=main_menu_keyboard(),
        )
        return

    if not result["success"] and result.get("search_configured") is False:
        await state.clear()
        await message.answer(
            search_not_configured_text(),
            reply_markup=main_menu_keyboard(),
        )
        return

    if not result["success"]:
        await state.clear()
        await message.answer(
            search_error_text(),
            reply_markup=main_menu_keyboard(),
        )
        return

    await state.clear()

    if not result["records"]:
        await message.answer(
            no_results_text(),
            reply_markup=main_menu_keyboard(),
        )
        return

    await message.answer(
        result["formatted_text"],
        reply_markup=main_menu_keyboard(),
    )
