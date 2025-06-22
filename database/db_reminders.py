import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timezone#, timedelta

from .database import async_session
from .models import Reminder

from sqlalchemy import select

import logging

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler() 

async def add_user_reminder(
    *,
    user_id: int,
    reminder_date: datetime,
    reminder_text: str,
    is_sent: bool = False
) -> None:
    async with async_session() as session:
        reminder = Reminder(
            user_id=user_id,
            reminder_date=reminder_date,
            reminder_text=reminder_text,
            is_sent=is_sent
        )
        session.add(reminder)
        await session.commit()
        
        logger.info(
            "Reminder added. Table='%s', user_id=%d, "
            "reminder_date='%s', reminder_text='%s'",
            "reminders",
            user_id,
            reminder_date,
            reminder_text
        )
            
async def get_user_reminders(user_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(Reminder).where(Reminder.user_id == user_id)
        )
        return result.scalars().all()

async def check_reminders():
    async with async_session() as session:
        result = await session.execute(
            select(Reminder).where(Reminder.reminder_date <= datetime.now(timezone.utc), Reminder.is_sent == False)    
        )
        reminders = result.scalars().all()
        
        for reminder in reminders:
            user_id = reminder.user_id
            reminder_text = reminder.reminder_text
            
            # Обычное логирование -> прикрутить логику
            logger.info(f"Sending reminder to user {user_id}: {reminder_text}")
            
            reminder.is_sent = True
            await session.commit()

async def start_scheduler():
    
    scheduler.add_job(
        check_reminders,
        IntervalTrigger(minutes=1)
    )
    
    scheduler.start()
    
    while True:
        await asyncio.sleep(1)
        
