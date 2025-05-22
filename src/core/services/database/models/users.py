from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import  String
from typing import Optional
import bcrypt
import logging

from src.core.services.database.models.base import Base, int_pk, created_at, updated_at


logger = logging.getLogger(__name__)

class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int_pk]
    login: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True) # Login for autorization
    username: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, default='Anonymous') # Username for public name. Can be none -> Anonymous 
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    join_data: Mapped[created_at]
    last_time_login: Mapped[updated_at]
    is_active: Mapped[bool] = mapped_column(default=False)
    is_super_user: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"<User(id={self.id}, login={self.login})>"
    
    def set_password(self):
        """Securely hash and store password"""
        self.password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode()

    def check_password(self, plaintext_password: str) -> bool:
        """Verify password with automatic format correction"""
            
        try:
            return bcrypt.checkpw(plaintext_password.encode('utf-8'), self.password.encode('utf-8'))
        except Exception as err:
            logger.error(f"Password verification failed for user {self.id}: {err}. {__name__}")
            return False
