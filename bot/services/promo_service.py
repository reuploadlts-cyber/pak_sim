from datetime import datetime

from bot.database.crud import (
    create_promo_usage,
    get_promo_code_by_code,
    has_user_used_promo,
    increment_promo_used_count,
)
from bot.services.coin_service import add_coins, get_coin_balance


def _parse_utc_text(value: str) -> datetime | None:
    raw = value.strip()
    if raw.endswith(" UTC"):
        raw = raw[:-4]
    try:
        return datetime.strptime(raw, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def redeem_promo_code(telegram_id: int, raw_code: str) -> dict:
    code = raw_code.strip()
    if not code:
        return {"status": "invalid"}

    promo = get_promo_code_by_code(code)
    if promo is None:
        return {"status": "invalid"}

    if int(promo["is_active"]) != 1:
        return {"status": "inactive"}

    expires_at = promo["expires_at"]
    if expires_at:
        expires_at_dt = _parse_utc_text(str(expires_at))
        if expires_at_dt and datetime.utcnow() > expires_at_dt:
            return {"status": "expired"}

    if int(promo["used_count"]) >= int(promo["max_uses"]):
        return {"status": "limit_reached"}

    if has_user_used_promo(int(promo["id"]), telegram_id):
        return {"status": "already_used"}

    reward_coins = int(promo["reward_coins"])

    added = add_coins(
        telegram_id=telegram_id,
        amount=reward_coins,
        reason=f"promo_code:{promo['code']}",
    )
    if not added:
        return {"status": "error"}

    create_promo_usage(
        promo_code_id=int(promo["id"]),
        user_id=telegram_id,
    )
    increment_promo_used_count(int(promo["id"]))

    new_balance = get_coin_balance(telegram_id)
    if new_balance is None:
        return {"status": "error"}

    return {
        "status": "success",
        "code": str(promo["code"]),
        "coins_added": reward_coins,
        "new_balance": new_balance,
    }
