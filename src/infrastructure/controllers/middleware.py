import hashlib

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from src.application.errors import ApplicationError, ArticleNotFoundError


class TokenAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, token: str):
        super().__init__(app)
        self._token = token

    async def dispatch(self, request: Request, call_next):
        if request.method == "POST":
            x_sign = request.headers.get("X-Sign")
            x_time = request.headers.get("X-Time")

            if not x_sign or not x_time:
                return JSONResponse(
                    status_code=400,
                    content={"detail": "Missing X-Sign or X-Time header."},
                )

            body = await request.body()
            payload = body.decode("utf-8") if body else ""

            computed_sign = hashlib.sha256(
                f"{self._token}{payload}{x_time}".encode("utf-8")
            ).hexdigest()

            if x_sign != computed_sign:
                raise HTTPException(status_code=401, detail="Invalid signature.")

        return await call_next(request)


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

        except:
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"},
            )
