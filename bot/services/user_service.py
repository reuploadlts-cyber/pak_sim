from bot.config import settings
from bot.constants import START_REF_PREFIX
from bot.database.crud import (
    create_user,
    get_user_by_referral_code,
    get_user_by_telegram_id,
    increment_user_total_searches,
    update_user_basic_info,
)


def build_referral_code(telegram_id: int) -> str:
    return f"{START_REF_PREFIX}{telegram_id}"


def build_referral_link(referral_code: str) -> str:
    return f"https://t.me/{settings.bot_username}?start={referral_code}"


def register_or_update_user(
    telegram_id: int,
    full_name: str,
    username: str | None,
    start_arg: str | None = None,
):
    existing_user = get_user_by_telegram_id(telegram_id)

    if existing_user is None:
        referred_by: int | None = None

        if start_arg and start_arg.startswith(START_REF_PREFIX):
            ref_owner = get_user_by_referral_code(start_arg)
            if ref_owner and ref_owner["telegram_id"] != telegram_id:
                referred_by = ref_owner["telegram_id"]

        create_user(
            telegram_id=telegram_id,
            full_name=full_name,
            username=username,
            coins=settings.default_new_user_coins,
            referral_code=build_referral_code(telegram_id),
            referred_by=referred_by,
            referral_reward_coins=settings.referral_reward_coins,
        )
        return get_user_by_telegram_id(telegram_id)

    update_user_basic_info(
        telegram_id=telegram_id,
        full_name=full_name,
        username=username,
    )
    return get_user_by_telegram_id(telegram_id)


def get_user(telegram_id: int):
    return get_user_by_telegram_id(telegram_id)


def get_account_summary(telegram_id: int) -> dict | None:
    user = get_user_by_telegram_id(telegram_id)
    if user is None:
        return None

    referral_link = build_referral_link(user["referral_code"])

    return {
        "telegram_id": user["telegram_id"],
        "full_name": user["full_name"],
        "username": user["username"],
        "coins": user["coins"],
        "total_searches": user["total_searches"],
        "referral_count": user["referral_count"],
        "joined_at": user["joined_at"],
        "referral_link": referral_link,
    }


def get_user_coins(telegram_id: int) -> int | None:
    user = get_user_by_telegram_id(telegram_id)
    if user is None:
        return None
    return user["coins"]


def get_referral_summary(telegram_id: int) -> dict | None:
    user = get_user_by_telegram_id(telegram_id)
    if user is None:
        return None

    return {
        "referral_link": build_referral_link(user["referral_code"]),
        "referral_count": user["referral_count"],
    }


def add_search_count(telegram_id: int) -> None:
    increment_user_total_searches(telegram_id)
