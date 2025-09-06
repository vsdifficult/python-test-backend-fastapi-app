from pydantic import BaseModel 
from src.models.enums import UserRole 
import uuid

class AuthModel(BaseModel):
    success: bool
    user_id: uuid.UUID
    role: UserRole
    access_token: str
    refresh_token: str
