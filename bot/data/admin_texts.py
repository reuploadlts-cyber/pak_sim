def admin_panel_text() -> str:
    return (
        "⚙️ <b>Admin Panel</b>\n\n"
        "Available commands:\n\n"
        "/stats\n"
        "/userinfo &lt;telegram_id&gt;\n"
        "/addcoins &lt;telegram_id&gt; &lt;amount&gt;\n"
        "/removecoins &lt;telegram_id&gt; &lt;amount&gt;\n"
        "/ban &lt;telegram_id&gt;\n"
        "/unban &lt;telegram_id&gt;\n"
        "/broadcast &lt;message&gt;\n"
        "/addforce &lt;title&gt; | &lt;url&gt; | &lt;chat_id optional&gt;\n"
        "/listforce\n"
        "/removeforce &lt;link_id&gt;\n"
        "/createpromo &lt;code&gt; &lt;coins&gt; &lt;max_uses&gt;\n"
        "/disablepromo &lt;code&gt;\n"
        "/promoinfo &lt;code&gt;\n"
        "/health\n"
        "/backup"
    )


def stats_text(total_users: int, banned_users: int) -> str:
    return (
        "📊 <b>Bot Statistics</b>\n\n"
        f"👥 <b>Total Users:</b> {total_users}\n"
        f"🚫 <b>Banned Users:</b> {banned_users}"
    )


def user_info_text(user: dict) -> str:
    username = f"@{user['username']}" if user["username"] else "Not set"
    return (
        "👤 <b>User Info</b>\n\n"
        f"🆔 <b>ID:</b> <code>{user['telegram_id']}</code>\n"
        f"👤 <b>Name:</b> {user['full_name']}\n"
        f"🔗 <b>Username:</b> {username}\n"
        f"🪙 <b>Coins:</b> {user['coins']}\n"
        f"🔎 <b>Searches:</b> {user['total_searches']}\n"
        f"🎁 <b>Referrals:</b> {user['referral_count']}\n"
        f"🚫 <b>Banned:</b> {'Yes' if int(user['is_banned']) else 'No'}"
    )


def force_links_text(links: list[dict]) -> str:
    if not links:
        return "ℹ️ <b>No force join links found.</b>"

    lines = ["🔗 <b>Force Join Links</b>", ""]
    for link in links:
        lines.append(
            f"ID: <code>{link['id']}</code>\n"
            f"Title: {link['title']}\n"
            f"URL: {link['url']}\n"
            f"Chat ID: {link['chat_id'] or 'Not set'}\n"
            f"Active: {'Yes' if int(link['is_active']) else 'No'}"
        )
        lines.append("")
    return "\n".join(lines).strip()


def promo_info_text(promo: dict) -> str:
    return (
        "🎟 <b>Promo Info</b>\n\n"
        f"🔑 <b>Code:</b> {promo['code']}\n"
        f"🪙 <b>Reward Coins:</b> {promo['reward_coins']}\n"
        f"👥 <b>Max Uses:</b> {promo['max_uses']}\n"
        f"✅ <b>Used Count:</b> {promo['used_count']}\n"
        f"⚡ <b>Active:</b> {'Yes' if int(promo['is_active']) else 'No'}\n"
        f"⏰ <b>Expires At:</b> {promo['expires_at'] or 'No expiry'}"
    )


def health_text(
    db_ok: bool,
    total_users: int,
    total_force_links: int,
) -> str:
    return (
        "🩺 <b>Bot Health</b>\n\n"
        f"🗄 <b>Database:</b> {'OK' if db_ok else 'Failed'}\n"
        f"👥 <b>Total Users:</b> {total_users}\n"
        f"🔗 <b>Force Join Links:</b> {total_force_links}"
    )
