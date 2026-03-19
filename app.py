import asyncio
import logging
import os

from bot.database.session import init_db
from bot.handlers.admin import router as admin_router
from bot.handlers.fallback import router as fallback_router
from bot.handlers.promo import router as promo_router
from bot.handlers.referral import router as referral_router
from bot.handlers.search import router as search_router
from bot.handlers.start import router as start_router
from bot.handlers.user import router as user_router
from bot.loader import bot, dp
from bot.utils.logger import setup_logging


async def main() -> None:
    os.makedirs("storage", exist_ok=True)
    os.makedirs("storage/backups", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    setup_logging()
    await init_db()

    dp.include_router(start_router)
    dp.include_router(user_router)
    dp.include_router(search_router)
    dp.include_router(referral_router)
    dp.include_router(promo_router)
    dp.include_router(admin_router)
    dp.include_router(fallback_router)

    logging.info("Bot is starting polling...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")
