from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, BigInteger, Boolean, TIMESTAMP, ForeignKey, text
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("TIMEZONE('utc', now())"), nullable=False)
    role: Mapped[str] = mapped_column(String(5), nullable=False)
    is_alive: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    banned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    reminders = relationship("Reminder", back_populates="user", cascade="all, delete")
    
    def __repr__(self):
        return f"User(id={self.id}, user_id={self.user_id}, username={self.username}, role={self.role}, created_at={self.created_at}, is_alive={self.is_alive}, banned={self.banned})"
    
class Reminder(Base):
    __tablename__ = "reminders"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    reminder_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("TIMEZONE('utc', now())"), nullable=False)
    reminder_text: Mapped[str] = mapped_column(String(500), nullable=False)
    is_sent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    user = relationship("User", back_populates="reminders")
    
    def __repr__(self):
        return f"User(id={self.id}, user_id={self.user_id}, reminder_date={self.reminder_date}, reminder_text={self.reminder_text}, is_sent={self.is_sent}"