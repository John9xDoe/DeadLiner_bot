import asyncio
from datetime import datetime, timezone
from db_users import add_user, get_user, change_user_alive_status, change_user_banned_status, get_user_alive_status, get_user_banned_status
from db_reminders import add_user_reminder, get_user_reminders, check_reminders, start_scheduler
from create_tables import init_models
from sqlalchemy import BigInteger

async def test_add_user(user_id: BigInteger):
    data = {
        "user_id": user_id,
        "username": str(chr(user_id)),
        "created_at": datetime.now(timezone.utc)
    }
    
    await add_user(**data)
    
async def test_get_user(user_id: BigInteger):
    res = await get_user(user_id=user_id)
    return res

async def main():
    await init_models()
    
    #await change_user_alive_status(is_alive=False, user_id=0)
    #await change_user_banned_status(banned=True, user_id=1)
    
    print(await get_user_alive_status(user_id=0), await get_user_banned_status(user_id=1), sep='\n')
    
    #asyncio.run(start_scheduler())
    
    '''
    scheduler_task = asyncio.create_task(start_scheduler())
    
    await add_user_reminder(
        user_id=0,
        reminder_date=datetime(2025, 6, 21, 13, 52, 0),
        reminder_text='a1'
    )

    print(await get_user_reminders(user_id=0))
    
    await scheduler_task
    '''
    
if __name__ == '__main__':
    #asyncio.run(main())
    asyncio.get_event_loop().run_until_complete(main())