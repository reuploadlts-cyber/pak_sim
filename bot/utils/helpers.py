from aiogram.types import Message


def get_start_argument(message: Message) -> str | None:
    if not message.text:
        return None

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return None

    value = parts[1].strip()
    return value or None
