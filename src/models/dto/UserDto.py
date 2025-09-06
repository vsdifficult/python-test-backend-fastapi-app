from pydantic import BaseModel
from src.models.enums import UserRole
import uuid

class UserRegistration(BaseModel):
    name: str
    email: str
    password: str
    role: UserRole = UserRole.USER

class UserLogin(BaseModel):
    email: str
    password: str

class UserDto(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    password: str
    role: UserRole
    code: int | None = None
    code_expire: str | None = None

