from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from app.bot.enums.roles import UserRole
from database.db_users import get_user_role

class UserRoleFilter(BaseFilter):
    def __init__(self, *roles: str | UserRole): 
        if not roles:
            raise ValueError("At least one role must be provided to UserRoleFilter.")
                
        self.roles = frozenset(
            UserRole(role) if isinstance(role, str) else role
            for role in roles
            if isinstance(role, (str, UserRole))
        )
        
        if not self.roles:
            raise ValueError("No valid roles provided to `UserRoleFilter`.")
    
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        user = event.from_user
        
        if not user:
            return False

        role = await get_user_role(user_id=user.id)
        
        if role is None:
            return False
        
        return role in self.roles