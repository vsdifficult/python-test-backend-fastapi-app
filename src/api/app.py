from fastapi import FastAPI
from src.api.routes import auth
from src.api.middlewares.auth_middleware import AuthMiddleware
from src.api.middlewares.logging_middleware import LoggingMiddleware
from src.api.middlewares.error_handler import AuthErrorMiddleware
from src.database import init_db 

app = FastAPI(title="Auth API with Middleware")

@app.on_event("startup")
async def on_startup():
    await init_db()

app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthErrorMiddleware)
app.add_middleware(AuthMiddleware)

app.include_router(auth.router)
