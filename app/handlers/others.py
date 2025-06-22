#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aiogram import Router
from aiogram.types import Message

others_router = Router()

@others_router.message()
async def process_unknown_command(message: Message):
    await message.reply('unknown command')