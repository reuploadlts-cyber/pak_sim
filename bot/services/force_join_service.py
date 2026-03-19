from typing import Any

from aiogram import Bot

from bot.database.crud import (
    add_force_join_link,
    deactivate_force_join_link,
    get_active_force_join_links,
    get_all_force_join_links,
)


def is_force_join_enabled() -> bool:
    return len(get_active_force_join_links()) > 0


def create_force_join_link(title: str, url: str, chat_id: str | None = None) -> int:
    return add_force_join_link(title=title, url=url, chat_id=chat_id)


def remove_force_join_link(link_id: int) -> bool:
    return deactivate_force_join_link(link_id)


def get_force_join_links() -> list[dict[str, Any]]:
    return get_active_force_join_links()


def get_all_force_links() -> list[dict[str, Any]]:
    return get_all_force_join_links()


async def is_user_joined_required_chats(bot: Bot, user_id: int) -> bool:
    links = get_force_join_links()

    if not links:
        return True

    for link in links:
        chat_id = link.get("chat_id")

        if not chat_id:
            continue

        try:
            member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            status = getattr(member, "status", "")
            if status in {"left", "kicked"}:
                return False
        except Exception:
            return False

    return True
