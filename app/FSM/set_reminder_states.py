from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery

from database.db_reminders import (
    add_user_reminder
)

from datetime import datetime

class SetReminderStates(StatesGroup):
    waiting_for_date = State()
    waiting_for_text = State()
    
set_reminder_states_router = Router()

@set_reminder_states_router.message(StateFilter(default_state))
async def process_set_reminder(message: Message, state: FSMContext):
    await message.answer("reminder_date: ")
    await state.set_state(SetReminderStates.waiting_for_date)
    
@set_reminder_states_router.message(StateFilter(SetReminderStates.waiting_for_date))
async def process_date(message: Message, state: FSMContext):
    await state.update_data(reminder_date=message.text)
    
    await message.answer("reminder_text: ")
    await state.set_state(SetReminderStates.waiting_for_text)
    
@set_reminder_states_router.message(StateFilter(SetReminderStates.waiting_for_text))
async def process_text(message: Message, state: FSMContext):
    await state.update_data(reminder_text=message.text)
    
    data = await state.get_data()
    await add_user_reminder(
        user_id=message.from_user.id,
        reminder_date=datetime.strptime(data.get("reminder_date"), '%Y-%m-%d %H:%M:%S'),
        reminder_text=data.get("reminder_text")
        )
    await state.clear()
    
