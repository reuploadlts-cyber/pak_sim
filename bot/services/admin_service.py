import os
import shutil

from bot.config import settings
from bot.database.crud import (
    create_admin_log,
    create_promo_code,
    disable_promo_code,
    get_all_user_ids,
    get_promo_code_by_code,
    get_total_banned_users,
    get_total_users,
    get_user_by_telegram_id,
    set_user_ban_status,
)
from bot.services.coin_service import add_coins, deduct_coins
from bot.services.force_join_service import (
    create_force_join_link,
    get_all_force_links,
    remove_force_join_link,
)


def get_stats() -> dict:
    return {
        "total_users": get_total_users(),
        "banned_users": get_total_banned_users(),
    }


def get_user_info(telegram_id: int):
    return get_user_by_telegram_id(telegram_id)


def admin_add_coins(admin_id: int, user_id: int, amount: int) -> bool:
    success = add_coins(
        telegram_id=user_id,
        amount=amount,
        reason="admin_add",
        admin_id=admin_id,
    )
    if success:
        create_admin_log(
            admin_id=admin_id,
            action="add_coins",
            target_user_id=user_id,
            details=f"amount={amount}",
        )
    return success


def admin_remove_coins(admin_id: int, user_id: int, amount: int) -> bool:
    success = deduct_coins(
        telegram_id=user_id,
        amount=amount,
        reason="admin_remove",
        admin_id=admin_id,
    )
    if success:
        create_admin_log(
            admin_id=admin_id,
            action="remove_coins",
            target_user_id=user_id,
            details=f"amount={amount}",
        )
    return success


def ban_user(admin_id: int, user_id: int) -> bool:
    success = set_user_ban_status(user_id, 1)
    if success:
        create_admin_log(
            admin_id=admin_id,
            action="ban_user",
            target_user_id=user_id,
        )
    return success


def unban_user(admin_id: int, user_id: int) -> bool:
    success = set_user_ban_status(user_id, 0)
    if success:
        create_admin_log(
            admin_id=admin_id,
            action="unban_user",
            target_user_id=user_id,
        )
    return success


def add_force_link(admin_id: int, title: str, url: str, chat_id: str | None = None) -> int:
    link_id = create_force_join_link(title=title, url=url, chat_id=chat_id)
    create_admin_log(
        admin_id=admin_id,
        action="add_force_link",
        details=f"id={link_id}, title={title}, url={url}, chat_id={chat_id}",
    )
    return link_id


def list_force_links() -> list[dict]:
    return get_all_force_links()


def remove_force_link(admin_id: int, link_id: int) -> bool:
    success = remove_force_join_link(link_id)
    if success:
        create_admin_log(
            admin_id=admin_id,
            action="remove_force_link",
            details=f"id={link_id}",
        )
    return success


def create_promo(
    admin_id: int,
    code: str,
    reward_coins: int,
    max_uses: int,
) -> bool:
    success = create_promo_code(
        code=code,
        reward_coins=reward_coins,
        max_uses=max_uses,
        created_by=admin_id,
        expires_at=None,
    )
    if success:
        create_admin_log(
            admin_id=admin_id,
            action="create_promo",
            details=f"code={code}, reward={reward_coins}, max_uses={max_uses}",
        )
    return success


def disable_promo(admin_id: int, code: str) -> bool:
    success = disable_promo_code(code)
    if success:
        create_admin_log(
            admin_id=admin_id,
            action="disable_promo",
            details=f"code={code}",
        )
    return success


def get_promo_info(code: str):
    return get_promo_code_by_code(code)


def get_health() -> dict:
    db_ok = os.path.exists(settings.database_path)
    return {
        "db_ok": db_ok,
        "total_users": get_total_users(),
        "total_force_links": len(get_all_force_links()),
    }


def create_backup(admin_id: int) -> str:
    source = settings.database_path
    if not os.path.exists(source):
        raise FileNotFoundError("Database file not found.")

    os.makedirs("storage/backups", exist_ok=True)
    backup_name = f"backup_{source.split('/')[-1].replace('.db', '')}.db"
    backup_path = os.path.join("storage/backups", backup_name)
    shutil.copy2(source, backup_path)

    create_admin_log(
        admin_id=admin_id,
        action="backup_db",
        details=backup_path,
    )
    return backup_path


def get_all_broadcast_user_ids() -> list[int]:
    return get_all_user_ids()
