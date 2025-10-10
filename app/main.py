from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi import status
from contextlib import asynccontextmanager
from database.session import engine, base
from core.logger import logger

from core.exception_handler import setup_exception_handlers
from fastapi.exceptions import RequestValidationError

from database.models.users import Users
from database.models.debates import Debates
from database.models.analysis import Analysis
from database.models.arguments import Arguments
from database.models.feedback import Feedback
from database.models.participants import Participants
from database.models.summaries import Summaries

from modules.auth.controller import router as auth_router


@asynccontextmanager
async def startup_event(app: FastAPI):
    try:
        with engine.connect() as conn:
            logger.info("✅ Database connected successfully!")

        base.metadata.create_all(bind=engine)
        yield
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")


app = FastAPI(lifespan=startup_event)

setup_exception_handlers(app)

app.include_router(auth_router)


@app.get("/test")
def home():
    return {"status": "Server is running"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error = exc.errors()[0]
    print(error)
    field = error.get("loc")[-1] if error.get("loc") else "field"
    message = error.get("msg", "Invalid input")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": f"{field.capitalize()} {message}.", "status_code": 422},
    )
