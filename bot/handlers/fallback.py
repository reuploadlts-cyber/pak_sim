from aiogram import F, Router
from aiogram.types import Message

from bot.data.texts import unknown_command_text, unknown_message_text
from bot.keyboards.reply import main_menu_keyboard

router = Router(name=__name__)


@router.message(F.text.startswith("/"))
async def unknown_command_handler(message: Message) -> None:
    await message.answer(
        unknown_command_text(),
        reply_markup=main_menu_keyboard(),
    )


@router.message()
async def unknown_message_handler(message: Message) -> None:
    await message.answer(
        unknown_message_text(),
        reply_markup=main_menu_keyboard(),
    )
