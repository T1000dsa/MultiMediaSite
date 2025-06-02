from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from logging.config import dictConfig
import logging
import uvicorn

from src.core.config.config import settings
from src.core.config.logger import LOG_CONFIG
from core.dependencies.db_helper import db_helper

from api.v1.endpoints.index import router as index_router
from api.v1.auth.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    dictConfig(LOG_CONFIG)
    logger = logging.getLogger(__name__)
    #logger.info(settings)
    
    yield  # FastAPI handles requests here

    try:
        await db_helper.dispose()
        logger.info("✅ Connection pool closed cleanly")
    except Exception as e:
        logger.warning(f"⚠️ Error closing connection pool: {e}")


app = FastAPI(lifespan=lifespan, title=settings.title.title)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # can alter with time
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(index_router)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
        log_config=LOG_CONFIG
    )