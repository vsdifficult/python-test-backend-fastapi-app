import uuid
import bcrypt
import jwt
import random
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.user_repository import UserRepository
from src.models.dto.UserDto import UserRegistration, UserLogin 
from src.models.dto.AuthDto import AuthModel
from src.models.enums import UserRole

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET", "fallback_secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

class AuthService:
    def __init__(self):
        self.repo = UserRepository()

    async def sign_up(self, session: AsyncSession, body: UserRegistration):
        if await self.repo.get_by_email(session, body.email):
            raise ValueError("User already exists")
        hashed = bcrypt.hashpw(body.password.encode(), bcrypt.gensalt()).decode()
        user = await self.repo.create(session, body.name, body.email, hashed, body.role.value)
        return {"message": "User registered successfully"}

    async def login(self, session: AsyncSession, body: UserLogin):
        user = await self.repo.get_by_email(session, body.email)
        if not user or not bcrypt.checkpw(body.password.encode(), user.password.encode()):
            raise ValueError("Invalid credentials")
        access_token = self._create_token(user.id, user.role, ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token, expire = self._create_refresh_token(user.id, user.role)
        await self.repo.save_refresh_token(session, user.id, refresh_token, expire)
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    async def send_verification_email(self, session: AsyncSession, email: str):
        code = random.randint(100000, 999999)
        expire_at = datetime.utcnow() + timedelta(minutes=10)
        return await self.repo.set_verification_code(session, email, code, expire_at)

    async def verification_email(self, session: AsyncSession, email: str, code: int):
        user = await self.repo.get_by_email(session, email)
        if not user:
            raise ValueError("User not found")
        if user.code != code or not user.code_expire or user.code_expire < datetime.utcnow():
            raise ValueError("Invalid or expired code")
        access_token = self._create_token(user.id, user.role, ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token, expire = self._create_refresh_token(user.id, user.role)
        await self.repo.save_refresh_token(session, user.id, refresh_token, expire)
        return AuthModel(success=True, user_id=user.id, role=UserRole(user.role), access_token=access_token, refresh_token=refresh_token)

    async def refresh(self, session: AsyncSession, token: str):
        refresh = await self.repo.get_refresh_token(session, token)
        if not refresh or refresh.expire_at < datetime.utcnow():
            raise ValueError("Refresh token expired")
        access_token = self._create_token(refresh.user_id, UserRole.USER, ACCESS_TOKEN_EXPIRE_MINUTES)
        return {"access_token": access_token, "refresh_token": token}

    def _create_token(self, user_id: str, role: str, expire_minutes: int):
        expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
        payload = {"sub": user_id, "role": role, "exp": expire}
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def _create_refresh_token(self, user_id: str, role: str):
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        payload = {"sub": user_id, "role": role, "exp": expire, "type": "refresh"}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token, expire
