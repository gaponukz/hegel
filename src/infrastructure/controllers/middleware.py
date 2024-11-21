from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from src.application.errors import ApplicationError, ArticleNotFoundError


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)

        except ArticleNotFoundError as app_error:
            return JSONResponse(
                status_code=404,
                content={"detail": str(app_error)},
            )

        except ApplicationError as app_error:
            return JSONResponse(
                status_code=400,
                content={"detail": str(app_error)},
            )

        except Exception as error:
            print(f"{error.__class__.__name__}: {error}")
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"},
            )
