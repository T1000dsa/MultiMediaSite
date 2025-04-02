from src.core.models.base import Base, int_pk, created_at, updated_at
from sqlalchemy.orm import Mapped, mapped_column
import bcrypt
from src.core.config import logger
from typing import Optional

class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int_pk]
    login: Mapped[str] = mapped_column(unique=True) # Login for autorization
    username: Mapped[Optional[str]] # Username for public name. Can be none -> Anonymous 
    password: Mapped[str]
    mail: Mapped[Optional[str]]
    bio: Mapped[Optional[str]]
    join_data: Mapped[created_at]
    last_time_login: Mapped[updated_at]
    is_active: Mapped[bool] = mapped_column(default=True, nullable=True)
    is_super_user: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
    
    def set_password(self, password: str):
        """Securely hash and store password"""
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

    def check_password(self, plaintext_password: str) -> bool:
        """Verify password with automatic format correction"""
            
        try:
            return bcrypt.checkpw(plaintext_password.encode('utf-8'), self.password.encode())
        except Exception as err:
            logger.error(f"Password verification failed for user {self.id}: {err}. {__name__}")
            return False
