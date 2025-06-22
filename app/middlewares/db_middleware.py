from aiogram.types import TelegramObject
#from sqlalchemy.ext.asyncio import AsyncSession
from migrations.create_tables import async_session

import logging

logger = logging.getLogger(__name__)

class DataBaseMiddleware:
    async def __call__(self, handler, event: TelegramObject, data: dict):
        async with async_session() as session:
            data['session'] = session
            try:
                return await handler(event, data)
            except Exception as e:
                logger.error(f"Error handling event: {e}")
                raise