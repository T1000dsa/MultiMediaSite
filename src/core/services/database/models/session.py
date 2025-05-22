from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import  String, ForeignKey
from datetime import datetime
import logging
import secrets

from src.core.services.database.models.base import Base, int_pk, created_at, updated_at


logger = logging.getLogger(__name__)

class SessionModel(Base):
    __tablename__ = 'session'

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    user_agent: Mapped[str] = mapped_column(String(255), nullable=True)
    ip_address: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    session_token: Mapped[str] = mapped_column(
        String(255), 
        unique=True,
        default=lambda: str(secrets.token_urlsafe(32)),
        index=True
    )

    def __repr__(self):
        return f"<SessionModel(id={self.id}, session_token={self.session_token})>"
    