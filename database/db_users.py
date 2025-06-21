# +
import logging
from datetime import datetime, timezone

from app.bot.enums.roles import UserRole
from .database import async_session
from .models import User

from sqlalchemy import select, BigInteger
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)

async def add_user(
    *,
    user_id: BigInteger,
    username: str | None = None,
    created_at: datetime | None = None,
    role: UserRole = UserRole.USER,
    is_alive: bool = True,
    banned: bool = False
) -> None:
    async with async_session() as session:
        try:     
            logger.info("Starting to add user withid=%d...", user_id)
            
            result = await session.execute(
                select(User).where(User.user_id == user_id)
            )
            existing_user = result.scalar_one_or_none()
            
            if existing_user is None:
                user = User(
                    user_id=user_id,
                    username=username,
                    created_at=datetime.now(timezone.utc),
                    role=role,
                    is_alive=is_alive,
                    banned=banned
                )
                session.add(user)
                logger.info("Committing transaction for user with id=%d...", user_id)
                await session.commit()
                logger.info(f"User {user_id} added successfully.")
                #session.refresh(user)
                
                logger.info(
                    "User added. Table='%s', user_id=%d, created_at='%s', "
                    "role='%s', is_alive='%s', banned='%s'",
                    "users",
                    user_id,
                    datetime.now(timezone.utc),
                    role,
                    is_alive,
                    banned                    
                )
            else:
                logger.info(f"User with ID {user_id} already exists.")
        except IntegrityError:
            await session.rollback()
            logger.warning("User with user_id='%d' already exists. Skipping...", user_id)
            
    
async def get_user(user_id: BigInteger) -> User | None:
    try:
        async with async_session() as session:
            logger.info(f"Fetching user with user_id={user_id}...")

            result = await session.execute(
                select(User).where(User.user_id == user_id)
            )
            user = result.scalar_one_or_none()          
            
            if user:
                return user
            else:
                return None
    except Exception as e:
        logger.error(f"No user with id={user_id} found in the database: {e}")
    
async def change_user_alive_status(
    *,
    is_alive: bool,
    user_id: BigInteger
) -> None:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.user_id == user_id)
        )
        user = result.scalar_one_or_none()
    
        if user:
            user.is_alive = is_alive
            await session.commit()
    logger.info("Updated 'is_alive' status to '%s' for user %d", is_alive, user_id)
    
async def change_user_banned_status(
    *,
    banned: bool,
    user_id: BigInteger
) -> None:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.user_id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if user:
            user.banned = banned
            await session.commit()
    logger.info("Updated 'banned' status to '%s' for user %d", banned, user_id)
    
async def get_user_alive_status(user_id: BigInteger) -> bool | None:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.user_id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if user:
            logger.info("The user with id=%d has the is_alive status is '%s'", user_id, user.is_alive)
            return user.is_alive
        else:
            logger.info("No user with id=%d found in the database", user_id)
            return None
        
async def get_user_banned_status(user_id: BigInteger) -> bool | None:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.user_id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if user:
            logger.info("The user with id=%d has the banned status is '%s'", user_id, user.banned)
            return user.banned
        else:
            logger.info("No user with id=%d found in the database", user_id)
            return None

async def get_user_role(user_id: BigInteger) -> UserRole | None:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.user_id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if user:
            logger.info("The user with id=%d has the role is '%s'", user_id, user.role)
            return user.role
        else:
            logger.info("No user with id=%d founded in the database", user_id)
            return None
        