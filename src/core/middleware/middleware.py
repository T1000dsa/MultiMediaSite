from fastapi import FastAPI, Request
import logging
from typing import Optional

from src.utils.time_check import time_checker
from src.core.dependencies.auth_injection import get_auth_service
from src.core.dependencies.db_helper import db_helper
from src.core.config.auth_config import SESSION_TOKEN

logger = logging.getLogger(__name__)

ignore_path = {'/.well-known', '/ws/'}

def init_token_middleware(app: FastAPI):
    @time_checker
    @app.middleware("http")
    async def refresh_token(request: Request, call_next):
        if any(request.url.path.startswith(path) for path in ignore_path):
            return await call_next(request)
        
        try:
            # Only proceed with auth check if token exists
            if SESSION_TOKEN in request.cookies:
                async with db_helper.async_session() as db:
                    auth_service = await get_auth_service(session=db)
                    refresh_response = await auth_service.refresh_logic(request)
                    if refresh_response:
                        return refresh_response
            
            return await call_next(request)
            
        except Exception as err:
            logger.error(f"Middleware error: {err}")
            return await call_next(request)