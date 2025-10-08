from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.session import engine, base
from utils.logger import logger
from models.users import Users
from models.debates import Debates
from models.analysis import Analysis
from models.arguments import Arguments
from models.feedback import Feedback
from models.participants import Participants
from models.summaries import Summaries



@asynccontextmanager
async def startup_event(app:FastAPI):
    try:
        with engine.connect() as conn:
            logger.info('✅ Database connected successfully!')
        
        base.metadata.create_all(bind=engine)
        yield
    except Exception as e:
        logger.error(f'❌ Database connection failed: {e}')


app = FastAPI(lifespan=startup_event)

@app.get('/test')
async def test():
    return {'server is running: ': 'true' }