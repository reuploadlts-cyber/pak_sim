from datetime import datetime, timezone
from typing import Any

from bot.database.session import get_connection


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def get_user_by_telegram_id(telegram_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE telegram_id = ?",
        (telegram_id,),
    )
    row = cursor.fetchone()
    connection.close()
    return row


def get_user_by_referral_code(referral_code: str):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE referral_code = ?",
        (referral_code,),
    )
    row = cursor.fetchone()
    connection.close()
    return row


def create_user(
    telegram_id: int,
    full_name: str,
    username: str | None,
    coins: int,
    referral_code: str,
    referred_by: int | None = None,
    referral_reward_coins: int = 0,
) -> None:
    connection = get_connection()
    cursor = connection.cursor()

    now = utc_now_iso()

    cursor.execute(
        """
        INSERT INTO users (
            telegram_id,
            full_name,
            username,
            coins,
            total_searches,
            referral_code,
            referred_by,
            referral_count,
            is_banned,
            joined_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, 0, ?, ?, 0, 0, ?, ?)
        """,
        (
            telegram_id,
            full_name,
            username,
            coins,
            referral_code,
            referred_by,
            now,
            now,
        ),
    )

    if referred_by:
        cursor.execute(
            """
            UPDATE users
            SET referral_count = referral_count + 1,
                coins = coins + ?,
                updated_at = ?
            WHERE telegram_id = ?
            """,
            (
                referral_reward_coins,
                now,
                referred_by,
            ),
        )

    connection.commit()
    connection.close()


def update_user_basic_info(
    telegram_id: int,
    full_name: str,
    username: str | None,
) -> None:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE users
        SET full_name = ?, username = ?, updated_at = ?
        WHERE telegram_id = ?
        """,
        (
            full_name,
            username,
            utc_now_iso(),
            telegram_id,
        ),
    )
    connection.commit()
    connection.close()


def get_active_force_join_links() -> list[dict[str, Any]]:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, title, url, chat_id, is_active, created_at
        FROM force_join_links
        WHERE is_active = 1
        ORDER BY id ASC
        """
    )
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]


def get_all_force_join_links() -> list[dict[str, Any]]:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, title, url, chat_id, is_active, created_at
        FROM force_join_links
        ORDER BY id ASC
        """
    )
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]


def add_force_join_link(title: str, url: str, chat_id: str | None = None) -> int:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO force_join_links (title, url, chat_id, is_active, created_at)
        VALUES (?, ?, ?, 1, ?)
        """,
        (
            title,
            url,
            chat_id,
            utc_now_iso(),
        ),
    )
    row_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return int(row_id)


def deactivate_force_join_link(link_id: int) -> bool:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE force_join_links
        SET is_active = 0
        WHERE id = ?
        """,
        (link_id,),
    )
    updated = cursor.rowcount > 0
    connection.commit()
    connection.close()
    return updated


def increment_user_total_searches(telegram_id: int) -> None:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE users
        SET total_searches = total_searches + 1,
            updated_at = ?
        WHERE telegram_id = ?
        """,
        (
            utc_now_iso(),
            telegram_id,
        ),
    )
    connection.commit()
    connection.close()


def update_user_coins(telegram_id: int, new_coins: int) -> None:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE users
        SET coins = ?, updated_at = ?
        WHERE telegram_id = ?
        """,
        (
            new_coins,
            utc_now_iso(),
            telegram_id,
        ),
    )
    connection.commit()
    connection.close()


def create_coin_log(
    user_id: int,
    amount: int,
    action_type: str,
    reason: str,
    admin_id: int | None = None,
) -> None:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO coin_logs (user_id, amount, action_type, reason, admin_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            amount,
            action_type,
            reason,
            admin_id,
            utc_now_iso(),
        ),
    )
    connection.commit()
    connection.close()


def get_promo_code_by_code(code: str):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT *
        FROM promo_codes
        WHERE LOWER(code) = LOWER(?)
        LIMIT 1
        """,
        (code,),
    )
    row = cursor.fetchone()
    connection.close()
    return row


def has_user_used_promo(promo_code_id: int, user_id: int) -> bool:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT 1
        FROM promo_code_usages
        WHERE promo_code_id = ? AND user_id = ?
        LIMIT 1
        """,
        (promo_code_id, user_id),
    )
    row = cursor.fetchone()
    connection.close()
    return row is not None


def increment_promo_used_count(promo_code_id: int) -> None:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE promo_codes
        SET used_count = used_count + 1
        WHERE id = ?
        """,
        (promo_code_id,),
    )
    connection.commit()
    connection.close()


def create_promo_usage(promo_code_id: int, user_id: int) -> None:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO promo_code_usages (promo_code_id, user_id, used_at)
        VALUES (?, ?, ?)
        """,
        (
            promo_code_id,
            user_id,
            utc_now_iso(),
        ),
    )
    connection.commit()
    connection.close()


def create_promo_code(
    code: str,
    reward_coins: int,
    max_uses: int,
    created_by: int,
    expires_at: str | None = None,
) -> bool:
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO promo_codes (
                code,
                reward_coins,
                max_uses,
                used_count,
                is_active,
                expires_at,
                created_by,
                created_at
            )
            VALUES (?, ?, ?, 0, 1, ?, ?, ?)
            """,
            (
                code,
                reward_coins,
                max_uses,
                expires_at,
                created_by,
                utc_now_iso(),
            ),
        )
        connection.commit()
        return True
    except Exception:
        return False
    finally:
        connection.close()


def disable_promo_code(code: str) -> bool:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE promo_codes
        SET is_active = 0
        WHERE LOWER(code) = LOWER(?)
        """,
        (code,),
    )
    updated = cursor.rowcount > 0
    connection.commit()
    connection.close()
    return updated


def get_total_users() -> int:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    connection.close()
    return int(count)


def get_total_banned_users() -> int:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE is_banned = 1")
    count = cursor.fetchone()[0]
    connection.close()
    return int(count)


def set_user_ban_status(telegram_id: int, status: int) -> bool:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE users
        SET is_banned = ?, updated_at = ?
        WHERE telegram_id = ?
        """,
        (
            status,
            utc_now_iso(),
            telegram_id,
        ),
    )
    updated = cursor.rowcount > 0
    connection.commit()
    connection.close()
    return updated


def get_all_user_ids() -> list[int]:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT telegram_id FROM users")
    rows = cursor.fetchall()
    connection.close()
    return [int(row["telegram_id"]) for row in rows]


def create_admin_log(
    admin_id: int,
    action: str,
    target_user_id: int | None = None,
    details: str | None = None,
) -> None:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO admin_logs (admin_id, action, target_user_id, details, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            admin_id,
            action,
            target_user_id,
            details,
            utc_now_iso(),
        ),
    )
    connection.commit()
    connection.close()


def is_user_banned(telegram_id: int) -> bool:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT is_banned FROM users WHERE telegram_id = ? LIMIT 1",
        (telegram_id,),
    )
    row = cursor.fetchone()
    connection.close()
    if row is None:
        return False
    return int(row["is_banned"]) == 1
