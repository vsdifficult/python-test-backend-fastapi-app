from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.entities.UserModels import UserEntity, RefreshTokenEntity
from src.models.dto import UserDto
from datetime import datetime

class UserRepository:
    async def get_by_email(self, session: AsyncSession, email: str):
        result = await session.execute(select(UserEntity).filter(UserEntity.email == email))
        user = result.scalar_one_or_none()
        return user

    async def create(self, session: AsyncSession, name: str, email: str, password: str, role: str):
        user = UserEntity(name=name, email=email, password=password, role=role)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def set_verification_code(self, session: AsyncSession, email: str, code: int, expire_at: datetime):
        user = await self.get_by_email(session, email)
        if user:
            user.code = code
            user.code_expire = expire_at
            await session.commit()
            return True
        return False

    async def save_refresh_token(self, session: AsyncSession, user_id: str, token: str, expire_at: datetime):
        refresh = RefreshTokenEntity(user_id=user_id, token=token, expire_at=expire_at)
        session.add(refresh)
        await session.commit()
        return refresh

    async def get_refresh_token(self, session: AsyncSession, token: str):
        result = await session.execute(select(RefreshTokenEntity).filter(RefreshTokenEntity.token == token))
        return result.scalar_one_or_none()
