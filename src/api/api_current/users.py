from fastapi import APIRouter, Depends
import logging
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.schemas.users import UserRead, UserBase
from src.core.models.db_helper import db_helper
from src.api.api_current.orm.users import create_user, give_all_users, give_one_user


logger = logging.getLogger(__name__)
router = APIRouter(prefix=settings.api_prefix.current.users) # prefix=settings.api_prefix.prefix


@router.post('/add_user')
async def create_user_endpoint(
    user_schema:UserBase,
    session:Annotated[AsyncSession, Depends(db_helper.session_getter)]
    ):
    result = await create_user(
        session=session, 
        user_create=user_schema
        )
    return {'res':result}
    

@router.get('/receive_users')
async def receive_users_endpoint(
    session:Annotated[AsyncSession, Depends(db_helper.session_getter)]
    ):
    result = await give_all_users(session=session)
    return {'res':result}
    

@router.get('/receive_user')
async def receive_user_endpoint(
    user_schema:UserRead,
    session:Annotated[AsyncSession, Depends(db_helper.session_getter)]
    ):
    result = await give_one_user(
        session=session, 
        user_read=user_schema)
    return {'res':result}