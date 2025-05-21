from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException

from src.core.config.config import settings
from core.services.database.models.users import UserRead, UserBase
from src.core.models.users import UserModel

