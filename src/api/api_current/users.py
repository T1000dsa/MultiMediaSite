
from fastapi import APIRouter, Depends, HTTPException
import logging
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

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
        try:
            result = await create_user(
                session=session, 
                user_create=user_schema
            )
            await session.commit()

            return {'res': result}
        
        except HTTPException as err:
            logger.debug(err)
            return {'exc':err}

    

@router.get('/receive_users')
async def receive_users_endpoint(
    session:Annotated[AsyncSession, Depends(db_helper.session_getter)]
    ):
    result = await give_all_users(session=session)
    return {'res':result, 'status_code':200}
    

@router.get('/receive_user/{user_id}')
async def receive_user_endpoint(
    user_id:int,
    session:Annotated[AsyncSession, Depends(db_helper.session_getter)]
    ):
    result = await give_one_user(
        session=session, 
        user_id=user_id)
    return {'res':result}