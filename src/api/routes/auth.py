from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_session
from src.core.services.authService import AuthService
from src.models.dto.UserDto import UserRegistration, UserLogin

router = APIRouter(prefix="/auth", tags=["Auth"])
service = AuthService()

@router.post("/register")
async def register(user: UserRegistration, session: AsyncSession = Depends(get_session)):
    try:
        return await service.sign_up(session, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(user: UserLogin, session: AsyncSession = Depends(get_session)):
    try:
        return await service.login(session, user)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/send-code")
async def send_code(email: str, session: AsyncSession = Depends(get_session)):
    ok = await service.send_verification_email(session, email)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "message": "Verification code sent"}

@router.post("/verify-code")
async def verify_code(email: str, code: int, session: AsyncSession = Depends(get_session)):
    try:
        return await service.verification_email(session, email, code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/refresh")
async def refresh(refresh_token: str, session: AsyncSession = Depends(get_session)):
    try:
        return await service.refresh(session, refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
