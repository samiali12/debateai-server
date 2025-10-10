from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from core.logger import logger


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"❌ Unexpected error: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500, content={"detail": "Something went wrong on the server."}
        )
