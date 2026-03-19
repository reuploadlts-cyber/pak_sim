from bot.services.settings_service import get_referral_reward_coins
from bot.services.user_service import get_referral_summary as get_user_referral_summary


def get_referral_summary(telegram_id: int) -> dict | None:
    summary = get_user_referral_summary(telegram_id)
    if summary is None:
        return None

    referral_count = int(summary["referral_count"])
    reward_per_referral = get_referral_reward_coins()

    return {
        "referral_link": summary["referral_link"],
        "referral_count": referral_count,
        "earned_coins": referral_count * reward_per_referral,
    }
