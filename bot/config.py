import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _parse_admins(value: str) -> list[int]:
    if not value.strip():
        return []

    result: list[int] = []
    for item in value.split(","):
        item = item.strip()
        if item.isdigit():
            result.append(int(item))
    return result


@dataclass
class Settings:
    bot_token: str
    bot_username: str
    admins: list[int]
    support_username: str
    support_id: str
    database_path: str
    default_new_user_coins: int
    referral_reward_coins: int
    search_cost_coins: int
    search_provider_enabled: bool
    search_provider_name: str
    search_provider_base_url: str
    search_provider_timeout: int


def load_settings() -> Settings:
    bot_token = os.getenv("BOT_TOKEN", "").strip()
    if not bot_token:
        raise ValueError("BOT_TOKEN is missing in environment variables.")

    return Settings(
        bot_token=bot_token,
        bot_username=os.getenv("BOT_USERNAME", "YourBotUsername").strip(),
        admins=_parse_admins(os.getenv("ADMINS", "")),
        support_username=os.getenv("SUPPORT_USERNAME", "@YourUsername").strip(),
        support_id=os.getenv("SUPPORT_ID", "123456789").strip(),
        database_path=os.getenv("DATABASE_PATH", "storage/bot.db").strip(),
        default_new_user_coins=int(os.getenv("DEFAULT_NEW_USER_COINS", "1")),
        referral_reward_coins=int(os.getenv("REFERRAL_REWARD_COINS", "1")),
        search_cost_coins=int(os.getenv("SEARCH_COST_COINS", "1")),
        search_provider_enabled=os.getenv("SEARCH_PROVIDER_ENABLED", "false").strip().lower() == "true",
        search_provider_name=os.getenv("SEARCH_PROVIDER_NAME", "custom").strip(),
        search_provider_base_url=os.getenv("SEARCH_PROVIDER_BASE_URL", "").strip(),
        search_provider_timeout=int(os.getenv("SEARCH_PROVIDER_TIMEOUT", "15")),
    )


settings = load_settings()
