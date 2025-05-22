from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete, join
from typing import Optional
from datetime import datetime, timedelta
import logging 

from src.core.services.database.models.session import SessionModel
from src.core.services.database.models.users import UserModel
from src.core.schemas.auth_schema import SessionSchema


logger = logging.getLogger(__name__)

async def create_session(session: AsyncSession, user_id:int, expire_data:timedelta) -> Optional[SessionModel]:
    logger.debug('inside create_session')
    try:
        expire_data = datetime.now() + expire_data
        token_data = SessionSchema(user_id=user_id, expires_at=expire_data)
        res = SessionSchema.model_validate(token_data, from_attributes=True)
        user_data = {i:k for i, k in res.model_dump().items()}
        logger.debug(f'before SessionModel {user_data}')
        new_data = SessionModel(**user_data)
        session.add(new_data)
        logger.debug('after add SessionModel')
        await session.commit()
        await session.refresh(new_data)  # Refresh to get any database-generated values
        logger.debug(f'Session creation has been successfully completed {new_data.id}')
        return new_data.id

    except Exception as err:
        logger.error(f"{err}")
        await session.rollback()
        raise err

async def select_session(session: AsyncSession, session_token:str) -> Optional[SessionModel]:
    try:
        query = select(SessionModel).where(SessionModel.session_token==session_token)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    except Exception as err:
        logger.error(f"err")
        raise err
    
async def select_session_by_id(session: AsyncSession, session_id:str) -> Optional[SessionModel]:
    try:
        query = select(SessionModel).where(SessionModel.id==session_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    except Exception as err:
        logger.error(f"err")
        raise err

async def updata_session(session: AsyncSession) -> None:pass

async def delete_session(session: AsyncSession,session_id:int) -> None:
    try:
        query = (delete(SessionModel).where(SessionModel.id==session_id))
        await session.execute(query)
        await session.commit()

    except Exception as err:
        logger.error(f"{err}")
        await session.rollback()
        raise err
    
async def cleanup_expired_sessions(session: AsyncSession):
    await session.execute(
        delete(SessionModel).where(SessionModel.expires_at < datetime.now())
    )
    await session.commit()