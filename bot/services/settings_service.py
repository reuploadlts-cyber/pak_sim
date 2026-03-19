from bot.config import settings


def get_support_username() -> str:
    return settings.support_username


def get_support_id() -> str:
    return settings.support_id


def get_default_new_user_coins() -> int:
    return settings.default_new_user_coins


def get_referral_reward_coins() -> int:
    return settings.referral_reward_coins


def get_search_cost_coins() -> int:
    return settings.search_cost_coins
