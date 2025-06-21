import logging

from aiogram import Bot, Router
from aiogram.enums import BotCommandScopeType
from aiogram.filters import KICKED, ChatMemberUpdatedFilter, Command, CommandStart
from aiogram.types import BotCommandScopeChat, ChatMemberUpdated, Message

from app.bot.enums.roles import UserRole
from app.bot.keyboards.menu_button import get_main_menu_commands
from database.db_users import (
    add_user, 
    change_user_alive_status, 
    get_user
)
from database.db_reminders import (
    add_reminder,
    get_reminders
)

from config.config import Config, load_config 

config: Config = load_config()

logger = logging.getLogger(__name__)

user_router = Router()

@user_router.message(CommandStart())
async def process_start_command(
    message: Message,
    bot: Bot,
    admin_ids: list[int] = config.bot.admin_ids
):
    user_row = await get_user(user_id=message.from_user.id)
    if user_row is None:
        if message.from_user.id in admin_ids:
            user_role = UserRole.ADMIN
        else: 
            user_role = UserRole.USER
        
        await add_user(
            user_id=message.from_user.id,
            username=message.from_user.username,
            role=user_role
        )
    else:
        print(user_row)
        user_role = UserRole(user_row.role)
        
        await change_user_alive_status(
            is_alive=True,
            user_id=message.from_user.id
        )
        
    await bot.set_my_commands(
        commands=get_main_menu_commands(role=user_role),
        scope = BotCommandScopeChat(
            type=BotCommandScopeType.CHAT,
            chat_id=message.from_user.id
        )
    )
    
    await message.answer('start_text')
    
@user_router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(text='help_text')
    
@user_router.message(Command(commands="set_reminder"))
async def set_reminder():
    pass
    
    
@user_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated):
    logger.info("User with id=%d has blocked the bot", event.from_user.id)
    await change_user_alive_status(is_alive=False, user_id=event.from_user.id)