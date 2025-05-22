from enum import Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.services.database.models.base import Base, int_pk, created_at
from .users import UserModel


class MediaType(str, Enum):
    VIDEO = "video"
    IMAGE = "image"
    AUDIO = "audio"

class MediaModel(Base):
    __tablename__ = "media"
    
    id: Mapped[int_pk]
    title: Mapped[str]
    file_path: Mapped[str]  # e.g., "uploads/user_1/video.mp4"
    media_type: Mapped[MediaType]
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    description: Mapped[str] = mapped_column(default=None, nullable=True)
    created_at: Mapped[created_at]