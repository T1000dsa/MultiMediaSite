# git push -u origin main
# git ls-files | xargs wc -l
# uvicorn src.main:app --reload

from fastapi import FastAPI
import logging
from contextlib import asynccontextmanager

from src.core.config import settings
from src.api.api_current.index import router as index_router
from src.api.api_current.users import router as users_router
from src.core.models.db_helper import db_helper
from src.core.models.base import Base
from src.core.models.users import UserModel

@asynccontextmanager
async def lifespan(app: FastAPI):

    yield
    
    try:
        await db_helper.dispose()
        logger.debug("✅ Connection pool closed cleanly")
    except Exception as e:
        logger.warning(f"⚠️ Error closing connection pool: {e}")


app = FastAPI(lifespan=lifespan)
logger = logging.getLogger(__name__)


app.include_router(index_router)
app.include_router(users_router)