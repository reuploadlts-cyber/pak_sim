from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from bot.constants import VERIFY_FORCE_JOIN_CALLBACK
from bot.data.texts import (
    banned_user_text,
    force_join_not_verified_text,
    force_join_required_text,
    force_join_verified_text,
    welcome_text,
)
from bot.database.crud import is_user_banned
from bot.keyboards.inline import force_join_keyboard
from bot.keyboards.reply import main_menu_keyboard
from bot.services.force_join_service import (
    get_force_join_links,
    is_force_join_enabled,
    is_user_joined_required_chats,
)
from bot.services.user_service import register_or_update_user
from bot.utils.helpers import get_start_argument

router = Router(name=__name__)


async def send_force_join_prompt(message: Message) -> None:
    links = get_force_join_links()

    if not links:
        await message.answer("Force join is enabled but no active links were found.")
        return

    await message.answer(
        force_join_required_text(),
        reply_markup=force_join_keyboard(links),
    )


async def ensure_access_or_prompt(message: Message) -> bool:
    tg_user = message.from_user
    if tg_user is None:
        return False

    if is_user_banned(tg_user.id):
        await message.answer(
            banned_user_text(),
            reply_markup=main_menu_keyboard(),
        )
        return False

    if not is_force_join_enabled():
        return True

    has_access = await is_user_joined_required_chats(
        bot=message.bot,
        user_id=tg_user.id,
    )

    if has_access:
        return True

    await send_force_join_prompt(message)
    return False


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    tg_user = message.from_user
    if tg_user is None:
        return

    user = register_or_update_user(
        telegram_id=tg_user.id,
        full_name=tg_user.full_name,
        username=tg_user.username,
        start_arg=get_start_argument(message),
    )

    if user and int(user["is_banned"]) == 1:
        await message.answer(
            banned_user_text(),
            reply_markup=main_menu_keyboard(),
        )
        return

    if is_force_join_enabled():
        has_access = await is_user_joined_required_chats(
            bot=message.bot,
            user_id=tg_user.id,
        )
        if not has_access:
            await send_force_join_prompt(message)
            return

    await message.answer(
        welcome_text(full_name=user["full_name"]),
        reply_markup=main_menu_keyboard(),
    )


@router.callback_query(F.data == VERIFY_FORCE_JOIN_CALLBACK)
async def verify_force_join_handler(callback: CallbackQuery) -> None:
    tg_user = callback.from_user
    if tg_user is None:
        await callback.answer()
        return

    if is_user_banned(tg_user.id):
        await callback.answer("Access denied.", show_alert=True)
        if callback.message:
            await callback.message.answer(
                banned_user_text(),
                reply_markup=main_menu_keyboard(),
            )
        return

    if not is_force_join_enabled():
        await callback.answer("No force join links configured.")
        if callback.message:
            await callback.message.answer(
                force_join_verified_text(full_name=tg_user.full_name),
                reply_markup=main_menu_keyboard(),
            )
        return

    has_access = await is_user_joined_required_chats(
        bot=callback.bot,
        user_id=tg_user.id,
    )

    if not has_access:
        await callback.answer("Join required channels/groups first.", show_alert=True)
        if callback.message:
            await callback.message.answer(
                force_join_not_verified_text(),
                reply_markup=force_join_keyboard(get_force_join_links()),
            )
        return

    await callback.answer("Verification successful.")
    if callback.message:
        await callback.message.answer(
            force_join_verified_text(full_name=tg_user.full_name),
            reply_markup=main_menu_keyboard(),
        )
