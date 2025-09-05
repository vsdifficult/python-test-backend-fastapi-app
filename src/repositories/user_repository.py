from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.dto.UserDto import UserDto
from src.models.entities.UserModels import UserEntity

import uuid 

class UserRepository:

    @staticmethod
    async def get_by_id(session: AsyncSession, user_id: uuid.UUID) -> UserDto | None:
        result = await session.execute(select(UserEntity).filter(UserEntity.id == user_id))
        user = result.scalar_one_or_none()
        return UserDto.model_validate(user.__dict__) if user else None

    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> UserDto | None:
        result = await session.execute(select(UserEntity).filter(UserEntity.email == email))
        user = result.scalar_one_or_none()
        return UserDto.model_validate(user.__dict__) if user else None

    @staticmethod
    async def create_async(session: AsyncSession, user_dto: UserDto) -> UserDto:
        user = UserEntity(**user_dto.model_dump())
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return UserDto.model_validate(user.__dict__) 
    
    @staticmethod 
    async def delete_async(session: AsyncSession, user_id: uuid.UUID) -> bool: 
        result = await session.execute(select(UserEntity).filter(UserEntity.id == user_id))
        user = result.scalar_one_or_none()
        if user: 
            await session.delete(user)
            await session.commit()
            return True 
        return False
