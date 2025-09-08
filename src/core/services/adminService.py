from src.domain.repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
import uuid 

class AdminService:
    def __init__(self):
        self.repo = UserRepository()

    async def delete_user_async(self, session: AsyncSession, user_id: uuid.UUID):
        return await self.repo.delete_user(session, user_id)  
    
    async def get_all_users_async(self, session: AsyncSession, offset: int = 0, limit: int = 100):
        return await self.repo.get_all_users(session, offset, limit)