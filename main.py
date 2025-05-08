import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers.user import user_router
from handlers.admin import admin_router
from database.db import init_db, create_tables

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# Register routers
dp.include_router(user_router)
dp.include_router(admin_router)

async def on_startup():
    """Actions to perform on bot startup"""
    try:
        # Initialize database connection pool
        await init_db()
        # Create database tables on startup
        await create_tables()
        logger.info("Bot started and database initialized")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        sys.exit(1)

async def main():
    """Main function to start the bot"""
    # Startup actions
    await on_startup()
    
    # Start polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
