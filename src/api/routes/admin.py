from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database import get_session
from src.core.services.adminService import AdminService

import uuid 

router = APIRouter(prefix="/admin", tags=["Auth"])
service = AdminService()

@router.post("/delete-user")
async def register(user_id: uuid.UUID, session: AsyncSession = Depends(get_session)): 
    ok = await service.delete_user_async(session, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return 

@router.get("/get-all-users")
async def register(session: AsyncSession = Depends(get_session), offset: int = 0, limit: int = 100): 
    return await service.get_all_users_async(session, offset, limit) 