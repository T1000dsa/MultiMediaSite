from fastapi import Request, Response, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime
import logging

from src.core.services.database.models.users import UserModel
from src.core.services.database.models.session import SessionModel
from src.core.services.database.orm.user_orm import (
    select_data_user, 
    insert_data,
    delete_data, 
    select_data_user_id,
    user_activate,
    select_user_email
    )

from src.core.services.database.orm.session_orm import (
    create_session,
    select_session,
    select_session_by_id,
    updata_session,
    delete_session
)
from src.core.config.auth_config import EXPIRE_TIME, SESSION_TOKEN


logger = logging.getLogger(__name__)

class AuthService:
    """Should have to use as a dependency"""
    def __init__(self, session: AsyncSession):
        self.session = session
        #self.token_service = token_service  # Use injected service
    
    async def create_user(self, **kwargs) -> None:
        await insert_data(self.session, **kwargs)

    async def delete_user(self, user_id:int) -> None:
        await delete_data(self.session, user_id)

    async def disable_user(self, user_id:int):
        await user_activate(self.session, user_id, False)

    async def activate_user(self, user_id:int):
        await user_activate(self.session, user_id, True)

    async def get_user_by_email(self, email:str) -> Optional[UserModel]:
        return await select_user_email(self.session, email)
    
    async def get_user_by_login(self, login: str, password:str) -> Optional[UserModel]:
        return await select_data_user(self.session, login, password)
    
    async def get_user_by_id(self, user_id:int) -> Optional[UserModel]:
        return await select_data_user_id(self.session, user_id)
    
    async def verify_user_tokens(self, request:Request) -> dict:
        pass
    
    async def gather_user_data(self, request:Request) -> dict:
        pass

    async def authenticate_user(self, login: str, password: str) -> Optional[SessionModel]: # Aka login
        logger.debug(f'User {login} tries to authorize...')
        try:
            user = await self.get_user_by_login(login, password)
            logger.debug(f'{user=}')
            if not user:
                return None
            
            logger.debug(f'Before activation...')
            await self.activate_user(user.id)

            logger.debug(f'Before create_session_db...')
            user_token_id = await self.create_session_db(user.id)

            logger.debug(f'Before return user_token... {user_token_id}')

            user_token = await select_session_by_id(session=self.session, session_id=user_token_id)
            return user_token
        except Exception as err:
            logger.error(f'{err}')
            raise err
        
    async def register_user(self, **kwargs):
        try:
            await self.create_user(kwargs)

        except Exception as err:
            logger.error(f'Something unexpectable: {err}')

    
    async def logout_user(self, response:Response) -> Response:
        response.delete_cookie("session_token")
        return response
    
    async def set_session_cookies(self, response:Response, cookie:SessionModel) -> Response:
        response.set_cookie(
            SESSION_TOKEN,
            cookie.session_token,
            httponly=True,     # Prevent XSS
            secure=True,       # HTTPS-only (ensure your site uses SSL)
            samesite="lax",    # Basic CSRF protection
            max_age=EXPIRE_TIME.seconds,      # 30-minute expiry (matches EXPIRE_TIME)
            )
        return response
    # Create a new session
    async def create_session_db(self, user_id: int) -> int:
        return await create_session(self.session, user_id, EXPIRE_TIME)
    
    # Validate session
    async def validate_session(self, request:Request) -> Optional[str]:
        session_token = request.cookies.get(SESSION_TOKEN)
        select_data_check = await select_session(self.session, session_token)
        if not select_data_check:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
        # Check if session has expired
        if datetime.now() > select_data_check.expires_at:
            await delete_session(self.session, select_data_check.id)

        user = await self.get_user_by_id(select_data_check.user_id)
        return user

    # Dependency to check for valid session
    async def get_current_user(self, request: Request):
        session_token = request.cookies.get(SESSION_TOKEN)
        if not session_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
        
        username = self.validate_session(request)
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired session"
            )
        
        return username