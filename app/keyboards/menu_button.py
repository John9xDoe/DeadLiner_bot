from aiogram.types import BotCommand 
from app.enums.roles import UserRole

def get_main_menu_commands(role: UserRole):
    if role == UserRole.USER:
        return [
            BotCommand(
                command='/start',
                description='start_description'
            ),
            BotCommand(
                command='/help',
                description='help_description'
            ),
            BotCommand(
                command='/set_reminder',
                description='set_reminder_description'
            )
        ]
    elif role == UserRole.ADMIN:
        return [
            BotCommand(
                command='/start',
                description='start_description'
            ),
            BotCommand(
                command='/help',
                description='help_description'
            ),
            BotCommand(
                command='/ban',
                description='ban_description'
            ),
            BotCommand(
                command='/unban',
                description='unban_description'
            )
        ]