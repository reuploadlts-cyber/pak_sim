from bot.config import settings


def welcome_text(full_name: str) -> str:
    return (
        f"👋 <b>Welcome, {full_name}!</b>\n\n"
        "Bot access successfully granted.\n"
        "Neeche menu se option choose karein."
    )


def force_join_required_text() -> str:
    return (
        "🔒 <b>Access Locked</b>\n\n"
        "Bot use karne ke liye pehle required channels/groups join karein.\n"
        "Join karne ke baad <b>Verify</b> button press karein."
    )


def force_join_not_verified_text() -> str:
    return (
        "❌ <b>Verification Failed</b>\n\n"
        "Abhi tak aap ne tamam required channels/groups join nahi kiye.\n"
        "Please pehle join karein, phir dobara <b>Verify</b> press karein."
    )


def force_join_verified_text(full_name: str) -> str:
    return (
        f"✅ <b>Verification Successful</b>\n\n"
        f"Welcome, <b>{full_name}</b>!\n"
        "Ab aap bot ki services use kar sakte hain."
    )


def banned_user_text() -> str:
    return (
        "🚫 <b>Access denied.</b>\n\n"
        "Aap ka account bot se blocked hai.\n"
        "Agar aap samajhte hain ke ye ghalti se hua hai to support se contact karein."
    )


def account_text(
    user_id: int,
    full_name: str,
    username: str | None,
    coins: int,
    total_searches: int,
    referral_count: int,
    joined_at: str,
    referral_link: str,
) -> str:
    username_text = f"@{username}" if username else "Not set"

    return (
        "👤 <b>Account Information</b>\n\n"
        f"🆔 <b>User ID:</b> <code>{user_id}</code>\n"
        f"👤 <b>Name:</b> {full_name}\n"
        f"🔗 <b>Username:</b> {username_text}\n"
        f"🪙 <b>Coins:</b> {coins}\n"
        f"🔎 <b>Total Searches:</b> {total_searches}\n"
        f"🎁 <b>Referrals:</b> {referral_count}\n"
        f"📅 <b>Joined:</b> {joined_at}\n\n"
        f"🔗 <b>Your Referral Link:</b>\n{referral_link}"
    )


def coins_text(coins: int) -> str:
    return (
        "🪙 <b>Your Coins</b>\n\n"
        f"You currently have <b>{coins}</b> coin(s)."
    )


def referral_text(
    referral_link: str,
    referral_count: int,
    earned_coins: int,
) -> str:
    return (
        "🎁 <b>Referral System</b>\n\n"
        f"🔗 <b>Your Referral Link:</b>\n{referral_link}\n\n"
        f"👥 <b>Total Referrals:</b> {referral_count}\n"
        f"🪙 <b>Earned Coins:</b> {earned_coins}\n"
        f"🎉 <b>Reward Per Referral:</b> {settings.referral_reward_coins} coin(s)"
    )


def redeem_prompt_text() -> str:
    return (
        "🎟 <b>Redeem Code</b>\n\n"
        "Apna promo code send karein.\n\n"
        "Cancel karne ke liye <b>cancel</b> likhein."
    )


def redeem_cancelled_text() -> str:
    return "❌ Promo code redeem cancelled."


def redeem_success_text(code: str, coins_added: int, new_balance: int) -> str:
    return (
        "✅ <b>Promo code redeemed successfully.</b>\n\n"
        f"🎟 <b>Code:</b> {code}\n"
        f"🪙 <b>Coins Added:</b> {coins_added}\n"
        f"💰 <b>New Balance:</b> {new_balance}"
    )


def promo_invalid_text() -> str:
    return "❌ <b>Invalid promo code.</b>"


def promo_already_used_text() -> str:
    return "❌ <b>You have already used this promo code.</b>"


def promo_inactive_text() -> str:
    return "❌ <b>This promo code is inactive.</b>"


def promo_expired_text() -> str:
    return "❌ <b>This promo code has expired.</b>"


def promo_limit_reached_text() -> str:
    return "❌ <b>Promo code usage limit reached.</b>"


def promo_redeem_error_text() -> str:
    return (
        "⚠️ <b>Promo code redeem failed.</b>\n\n"
        "Please baad me dobara try karein."
    )


def search_prompt_text(search_cost: int) -> str:
    return (
        "🔍 <b>Search</b>\n\n"
        f"Har successful search par <b>{search_cost}</b> coin deduct hoga.\n"
        "Agar result na mila to coin deduct nahi hoga.\n\n"
        "📱 Mobile number zero ke baghair bhejein.\n"
        "✅ Example: <code>3123456789</code>\n\n"
        "🆔 CNIC 13 digits me without dashes bhejein.\n"
        "✅ Example: <code>3460112345678</code>"
    )


def search_processing_text() -> str:
    return "⏳ <b>Processing your search...</b>"


def search_invalid_mobile_zero_text() -> str:
    return (
        "❌ <b>Invalid mobile number format.</b>\n\n"
        "Number zero ke baghair bhejo.\n\n"
        "✅ Example: <code>3123456789</code>"
    )


def search_invalid_mobile_text() -> str:
    return (
        "❌ <b>Invalid mobile number format.</b>\n\n"
        "Pakistani mobile number zero ke baghair 10 digits me bhejein.\n\n"
        "✅ Example: <code>3123456789</code>"
    )


def search_invalid_cnic_text() -> str:
    return (
        "❌ <b>Invalid CNIC format.</b>\n\n"
        "CNIC 13 digits me without dashes bhejein.\n\n"
        "✅ Example: <code>3460112345678</code>"
    )


def search_invalid_input_text() -> str:
    return (
        "❌ <b>Invalid input.</b>\n\n"
        "Sirf valid mobile number ya valid 13-digit CNIC bhejein."
    )


def search_cancelled_text() -> str:
    return "❌ Search cancelled."


def help_text() -> str:
    return (
        "❓ <b>Help & Support</b>\n\n"
        "Kisi bhi issue, coins purchase, ya support ke liye contact karein:\n\n"
        f"👤 <b>Username:</b> {settings.support_username}\n"
        f"🆔 <b>Telegram ID:</b> <code>{settings.support_id}</code>"
    )


def user_not_found_text() -> str:
    return "User record not found. Please send /start first."


def no_results_text() -> str:
    return (
        "ℹ️ <b>No results found.</b>\n\n"
        "Is query par koi record available nahi mila.\n"
        "Is search par koi coin deduct nahi hua."
    )


def search_error_text() -> str:
    return (
        "⚠️ <b>Search failed.</b>\n\n"
        "Filhal result fetch nahi ho saka. Please baad me dobara try karein."
    )


def insufficient_coins_text(current_coins: int, required_coins: int) -> str:
    return (
        "❌ <b>Insufficient coins.</b>\n\n"
        f"🪙 Your Coins: <b>{current_coins}</b>\n"
        f"🔻 Required Coins: <b>{required_coins}</b>\n\n"
        "Search continue karne ke liye coins required hain."
    )


def search_not_configured_text() -> str:
    return (
        "⚙️ <b>Search service not configured.</b>\n\n"
        "Provider adapter abhi configured nahi hai.\n"
        "Isko <code>bot/services/api_client.py</code> me integrate kiya jata hai."
    )


def unknown_command_text() -> str:
    return (
        "❌ <b>Unknown command.</b>\n\n"
        "Please menu buttons use karein ya /start send karein."
    )


def unknown_message_text() -> str:
    return (
        "ℹ️ <b>Message not understood.</b>\n\n"
        "Please menu buttons use karein."
    )
