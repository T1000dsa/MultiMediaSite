from fastapi import APIRouter
import logging

from src.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter() # prefix=settings.api_prefix.prefix

@router.get('/')
async def index_function():
    return 'HELLO NEW PROJECT 0006!!!'