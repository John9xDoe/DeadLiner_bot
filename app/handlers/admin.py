#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from app.enums.roles import UserRole
from app.filters.filters import UserRoleFilter
from database.db_users import change_user_banned_status, get_user_banned_status

logger = logging.getLogger(__name__)

admin_router = Router()

admin_router.message.filter(UserRoleFilter(UserRole.ADMIN))

@admin_router.message(Command('help'))
async def process_admin_help_command(message: Message): #, LEXICON: dict
    await message.answer(text='admin_commands')
    
@admin_router.message(Command('ban'))
async def process_ban_command(message: Message, command: CommandObject):
    args = command.args
    
    if not args:
        await message.reply('empty_ban_answer')
        return
    
    arg_user = args.split()[0].strip()
    
    if arg_user.isdigit():
        banned_status = await get_user_banned_status(user_id=int(arg_user))
    else:
        await message.reply('incorrect_ban_arg')
        return
    
    if banned_status is None:
        await message.reply('no_user')
    elif banned_status:
        await message.reply('already_banned')
    else:
        await change_user_banned_status(banned=True, user_id=int(arg_user))
        await message.reply('succesfully_banned')
        
@admin_router.message(Command('unban'))
async def process_unban_command(message: Message, command: CommandObject):
    args = command.args
    
    if not args:
        await message.reply('empty_unban_answer')
        return
    
    arg_user = args.split()[0].strip()
    
    if arg_user.isdigit():
        banned_status = get_user_banned_status(user_id=int(arg_user))
    else:
        await message.reply('incorrect_unban_arg')
        return
    
    if banned_status is None:
        await message.reply('no_user')
    elif banned_status:
        await change_user_banned_status(banned=False, user_id=int(arg_user))
        await message.reply('succesfully_unbanned')
    else:
        await message.reply('not_banned')
        