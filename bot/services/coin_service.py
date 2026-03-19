from bot.database.crud import create_coin_log, get_user_by_telegram_id, update_user_coins


def get_coin_balance(telegram_id: int) -> int | None:
    user = get_user_by_telegram_id(telegram_id)
    if user is None:
        return None
    return int(user["coins"])


def has_enough_coins(telegram_id: int, required_amount: int) -> bool:
    balance = get_coin_balance(telegram_id)
    if balance is None:
        return False
    return balance >= required_amount


def add_coins(
    telegram_id: int,
    amount: int,
    reason: str,
    admin_id: int | None = None,
) -> bool:
    if amount <= 0:
        return False

    balance = get_coin_balance(telegram_id)
    if balance is None:
        return False

    new_balance = balance + amount
    update_user_coins(telegram_id=telegram_id, new_coins=new_balance)
    create_coin_log(
        user_id=telegram_id,
        amount=amount,
        action_type="credit",
        reason=reason,
        admin_id=admin_id,
    )
    return True


def deduct_coins(
    telegram_id: int,
    amount: int,
    reason: str,
    admin_id: int | None = None,
) -> bool:
    if amount <= 0:
        return False

    balance = get_coin_balance(telegram_id)
    if balance is None or balance < amount:
        return False

    new_balance = balance - amount
    update_user_coins(telegram_id=telegram_id, new_coins=new_balance)
    create_coin_log(
        user_id=telegram_id,
        amount=-amount,
        action_type="debit",
        reason=reason,
        admin_id=admin_id,
    )
    return True
