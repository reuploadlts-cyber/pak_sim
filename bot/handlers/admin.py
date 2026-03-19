from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

from bot.data.admin_texts import (
    admin_panel_text,
    force_links_text,
    health_text,
    promo_info_text,
    stats_text,
    user_info_text,
)
from bot.services.admin_service import (
    add_force_link,
    admin_add_coins,
    admin_remove_coins,
    ban_user,
    create_backup,
    create_promo,
    disable_promo,
    get_all_broadcast_user_ids,
    get_health,
    get_promo_info,
    get_stats,
    get_user_info,
    list_force_links,
    remove_force_link,
    unban_user,
)
from bot.utils.admin import is_admin

router = Router(name=__name__)


def admin_guard(message: Message) -> bool:
    user = message.from_user
    return user is not None and is_admin(user.id)


@router.message(Command("admin"))
async def admin_panel(message: Message) -> None:
    if not admin_guard(message):
        return
    await message.answer(admin_panel_text())


@router.message(Command("stats"))
async def stats_handler(message: Message) -> None:
    if not admin_guard(message):
        return

    stats = get_stats()
    await message.answer(
        stats_text(
            total_users=stats["total_users"],
            banned_users=stats["banned_users"],
        )
    )


@router.message(Command("userinfo"))
async def userinfo_handler(message: Message) -> None:
    if not admin_guard(message):
        return

    if not message.text:
        await message.answer("Usage: /userinfo <telegram_id>")
        return

    args = message.text.split(maxsplit=1)
    if len(args) != 2 or not args[1].isdigit():
        await message.answer("Usage: /userinfo <telegram_id>")
        return

    user = get_user_info(int(args[1]))
    if not user:
        await message.answer("User not found.")
        return

    await message.answer(user_info_text(dict(user)))


@router.message(Command("addcoins"))
async def addcoins_handler(message: Message) -> None:
    if not admin_guard(message):
        return

    if not message.text:
        await message.answer("Usage: /addcoins <id> <amount>")
        return

    args = message.text.split()
    if len(args) != 3 or not args[1].isdigit() or not args[2].isdigit():
        await message.answer("Usage: /addcoins <id> <amount>")
        return

    user_id = int(args[1])
    amount = int(args[2])

    success = admin_add_coins(message.from_user.id, user_id, amount)
    await message.answer("✅ Coins added." if success else "❌ Failed.")


@router.message(Command("removecoins"))
async def removecoins_handler(message: Message) -> None:
    if not admin_guard(message):
        return

    if not message.text:
        await message.answer("Usage: /removecoins <id> <amount>")
        return

    args = message.text.split()
    if len(args) != 3 or not args[1].isdigit() or not args[2].isdigit():
        await message.answer("Usage: /removecoins <id> <amount>")
        return

    user_id = int(args[1])
    amount = int(args[2])

    success = admin_remove_coins(message.from_user.id, user_id, amount)
    await message.answer("✅ Coins removed." if success else "❌ Failed.")


@router.message(Command("ban"))
async def ban_handler(message: Message) -> None:
    if not admin_guard(message):
        return

    if not message.text:
        await message.answer("Usage: /ban <id>")
        return

    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        await message.answer("Usage: /ban <id>")
        return

    success = ban_user(message.from_user.id, int(args[1]))
    await message.answer("🚫 User banned." if success else "❌ Failed.")


@router.message(Command("unban"))
async def unban_handler(message: Message) -> None:
    if not admin_guard(message):
        return

    if not message.text:
        await message.answer("Usage: /unban <id>")
        return

    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        await message.answer("Usage: /unban <id>")
        return

    success = unban_user(message.from_user.id, int(args[1]))
    await message.answer("✅ User unbanned." if success else "❌ Failed.")


@router.message(Command("broadcast"))
async def broadcast_handler(message: Message) -> None:
    if not admin_guard(message):
        return

    if not message.text:
        await message.answer("Usage: /broadcast <message>")
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) != 2 or not parts[1].strip():
        await message.answer("Usage: /broadcast <message>")
        return

    broadcast_text = parts[1].strip()
    user_ids = get_all_broadcast_user_ids()

    success_count = 0
    fail_count = 0

    for user_id in user_ids:
        try:
            await message.bot.send_message(user_id, broadcast_text)
            success_count += 1
        except Exception:
            fail_count += 1

    await message.answer(
        f"📢 Broadcast completed.\n\n✅ Success: {success_count}\n❌ Failed: {fail_count}"
    )


@router.message(Command("addforce"))
async def addforce_handler(message: Message) -> None:
    if not admin_guard(message):
        return

    if not message.text:
        await message.answer("Usage: /addforce <title> | <url> | <chat_id optional>")
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) != 2:
        await message.answer("Usage: /addforce <title> | <url> | <chat_id optional>")
        return

    payload = [item.strip() for item in parts[1].split("|")]
    if len(payload) < 2:
        await message.answer("Usage: /addforce <title> | <url> | <chat_id optional>")
        return

    title = payload[0]
    url = payload[1]
    chat_id = payload[2] if len(payload) > 2 and payload[2] else None

    link_id = add_force_link(
        admin_id=message.from_user.id,
        title=title,
        url=url,
        chat_id=chat_id,
    )

    await message.answer(f"✅ Force join link added with ID: <code>{link_id}</code>")


@router.message(Command("listforce"))
async def listforce_handler(message: Message) -> None:
    if not admin_guard(message):
        return

    links = list_force_links()
    await message.answer(force_links_text(links))


@router.message(Command("removeforce"))
async def removeforce_handler(message: Message) -> None:
    if not admin_guard(message):
        return

    if not message.text:
        await message.answer("Usage: /removeforce <link_id>")
        return

    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        await message.answer("Usage: /removeforce <link_id>")
        return

    success = remove_force_link(message.from_user.id, int(args[1]))
    await message.answer("✅ Force link removed." if success else "❌ Link not found.")


@router.message(Command("createpromo"))
async def createpromo_handler(message: Message) -> None:
    if not admin_guard(message):
        return

    if not message.text:
        await message.answer("Usage: /createpromo <code> <coins> <max_uses>")
        return

    args = message.text.split()
    if len(args) != 4 or not args[2].isdigit() or not args[3].isdigit():
        await message.answer("Usage: /createpromo <code> <coins> <max_uses>")
        return

    code = args[1].strip()
    reward_coins = int(args[2])
    max_uses = int(args[3])

    success = create_promo(
        admin_id=message.from_user.id,
        code=code,
        reward_coins=reward_coins,
        max_uses=max_uses,
    )
    await message.answer("✅ Promo created." if success else "❌ Failed. Code may already exist.")


@router.message(Command("disablepromo"))
async def disablepromo_handler(message: Message) -> None:
    if not admin_guard(message):
        return

    if not message.text:
        await message.answer("Usage: /disablepromo <code>")
        return

    args = message.text.split(maxsplit=1)
    if len(args) != 2:
        await message.answer("Usage: /disablepromo <code>")
        return

    success = disable_promo(message.from_user.id, args[1].strip())
    await message.answer("✅ Promo disabled." if success else "❌ Promo not found.")


@router.message(Command("promoinfo"))
async def promoinfo_handler(message: Message) -> None:
    if not admin_guard(message):
        return

    if not message.text:
        await message.answer("Usage: /promoinfo <code>")
        return

    args = message.text.split(maxsplit=1)
    if len(args) != 2:
        await message.answer("Usage: /promoinfo <code>")
        return

    promo = get_promo_info(args[1].strip())
    if not promo:
        await message.answer("Promo not found.")
        return

    await message.answer(promo_info_text(dict(promo)))


@router.message(Command("health"))
async def health_handler(message: Message) -> None:
    if not admin_guard(message):
        return

    health = get_health()
    await message.answer(
        health_text(
            db_ok=health["db_ok"],
            total_users=health["total_users"],
            total_force_links=health["total_force_links"],
        )
    )


@router.message(Command("backup"))
async def backup_handler(message: Message) -> None:
    if not admin_guard(message):
        return

    try:
        backup_path = create_backup(message.from_user.id)
        document = FSInputFile(backup_path)
        await message.answer_document(document=document, caption="✅ Database backup")
    except Exception as error:
        await message.answer(f"❌ Backup failed: {error}")
