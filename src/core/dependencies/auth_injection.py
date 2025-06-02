from fastapi import Depends, Request
from typing import Annotated, Optional
import logging

from src.core.services.auth.auth_manager import AuthService
from src.core.dependencies.db_helper import DBDI
from src.core.services.database.models.users import UserModel
from src.core.config.auth_config import SESSION_TOKEN, credentials_exception, inactive_user_exception

logger = logging.getLogger(__name__)

def get_token_from_cookie(request: Request) -> Optional[str]:
    return request.cookies.get(SESSION_TOKEN)

async def get_auth_service(
    session: DBDI
) -> AuthService:
    return AuthService(
        session=session
    )

async def get_current_user(
    request: Request,
    token: str = Depends(get_token_from_cookie),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserModel:
    if token is None:
        raise credentials_exception
    
    if token is None:
        raise credentials_exception
    
    try:
        user = await auth_service.validate_session(request)

        if user is None:
            raise credentials_exception
            
    except Exception as err:
        logger.error(f'{err}')
        raise err
        
    return user

async def get_current_active_user(
    current_user: UserModel = Depends(get_current_user)
) -> UserModel:
    if not current_user.is_active:
        raise inactive_user_exception
    return current_user

GET_AUTH_SERVICE = Annotated[AuthService, Depends(get_auth_service)]
GET_CURRENT_USER = Annotated[UserModel, Depends(get_current_user)]
GET_CURRENT_ACTIVE_USER = Annotated[UserModel, Depends(get_current_active_user)]