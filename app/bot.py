import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from app.bot.handlers.admin import admin_router
from app.bot.handlers.user import user_router
from app.bot.handlers.others import others_router
from app.bot.FSM.set_reminder_states import set_reminder_states_router

from config.config import Config
from database.create_tables import init_models  

logger = logging.getLogger(__name__)

async def main(config: Config) -> None:
    logger.info("Starting bot...")
    
    storage = RedisStorage(
        redis=Redis(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
            password=config.redis.password,
            username=config.redis.username
        )
    )
    
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    
    dp = Dispatcher(storage=storage) # (bot=bot)
    
    await init_models() 
    
    logger.info("Including routers...")
    dp.include_routers(
        admin_router, 
        user_router, 
        set_reminder_states_router,
        others_router
    )
    
    try:
        await dp.start_polling(
            bot,
            admin_ids=config.bot.admin_ids
        )  
    except Exception as e:
        logger.exception(e)
    finally:
        logger.info("Bot stopped")