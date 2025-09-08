from datetime import datetime
import uuid 

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.domain.models.entities.UserModels import UserEntity, RefreshTokenEntity
from src.domain.models.dto import UserDto

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

    async def get_by_id(self, session: AsyncSession, user_id: uuid.UUID):
        result = await session.execute(select(UserEntity).filter(UserEntity.id == user_id))
        user = result.scalar_one_or_none()
        return user

    async def delete_user(self, session: AsyncSession, user_id: uuid.UUID):
        user = await self.get_by_id(session, user_id)
        if user:
            await session.delete(user)
            return True
        return False

    async def get_all_users(self, session: AsyncSession, offset: int = 0, limit: int = 100):
        result = await session.execute(select(UserEntity).offset(offset).limit(limit))
        return result.scalars().all()

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
