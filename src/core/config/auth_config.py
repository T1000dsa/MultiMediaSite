from fastapi import HTTPException, status
from typing import Any, Dict
from datetime import timedelta


EXPIRE_TIME:timedelta = timedelta(minutes=1)
SESSION_TOKEN:str = 'session_token'

class AuthException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: Any = None,
        headers: Dict[str, str] | None = None,
        error: str | None = None,
        error_description: str | None = None
    ):
        if headers is None:
            headers = {"WWW-Authenticate": "Bearer"}
        if error:
            if not detail:
                detail = {}
            if isinstance(detail, dict):
                detail.update({"error": error})
                if error_description:
                    detail.update({"error_description": error_description})
        super().__init__(status_code=status_code, detail=detail, headers=headers)

credentials_exception = AuthException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error="Need to authorize",
            headers={"WWW-Authenticate": "Bearer"},
        )

inactive_user_exception = AuthException(
    error="inactive_user",
    error_description="The user is inactive"
)