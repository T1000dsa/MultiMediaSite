from fastapi import Depends
from typing import Annotated

from src.core.services.auth.auth_manager import AuthService
from src.core.dependencies.db_helper import DBDI
from src.core.services.database.models.users import UserModel
from src.core.config.config import settings

async def get_auth_service(
    session: DBDI
) -> AuthService:
    return AuthService(
        session=session
    )

GET_AUTH_SERVICE = Annotated[AuthService, Depends(get_auth_service)]
