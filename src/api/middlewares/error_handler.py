from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from src.core.errors.authError import AuthError

class AuthErrorMiddleware(BaseHTTPMiddleware):
    """
    Middleware для обработки кастомных AuthError
    """

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except AuthError as e:
            return JSONResponse(
                status_code=401,
                content={"success": False, "error": e.message}
            )
