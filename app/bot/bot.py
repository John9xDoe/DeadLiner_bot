import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.bot.handlers.admin import admin_router
from app.bot.handlers.user import user_router
from app.bot.handlers.others import others_router

from config.config import Config
from database.create_tables import init_models  

logger = logging.getLogger(__name__)

async def main(config: Config) -> None:
    logger.info("Starting bot...")

    await init_models() 
    
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    
    dp = Dispatcher() # (bot)
    
    logger.info("Including routers...")
    dp.include_routers(admin_router, user_router, others_router)
    
    try:
        await dp.start_polling(bot)  
    except Exception as e:
        logger.exception(e)
    finally:
        logger.info("Bot stopped")