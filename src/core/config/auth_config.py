from fastapi import HTTPException, status, Depends
from passlib.context import CryptContext
from typing import Any, Dict, Annotated
from datetime import datetime, timedelta

from src.core.config.config import settings

EXPIRE_TIME:timedelta = timedelta(minutes=30)
SESSION_TOKEN:str = 'session_token'