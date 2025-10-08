from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.session import engine
from utils.logger import logger



@asynccontextmanager
async def startup_event(app:FastAPI):
    try:
        with engine.connect() as conn:
            logger.info('✅ Database connected successfully!')
        yield
    except Exception as e:
        logger.error(f'❌ Database connection failed: {e}')


app = FastAPI(lifespan=startup_event)