from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from typing import List

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, exempt_routes: List[str] = None):
        super().__init__(app)
        self.exempt_routes = exempt_routes or []
        self.exempt_routes += [
            "/docs",
            "/openapi.json",
            "/redoc",
            "/auth/register",
            "/auth/login",
            "/auth/send-code",
            "/auth/verify-code"
        ]

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.exempt_routes:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
        
        token = auth_header.split(" ")[1]

        return await call_next(request)
