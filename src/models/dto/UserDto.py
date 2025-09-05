from pydantic import BaseModel
from src.models.enums import UserRole 

import uuid 

class UserDto(BaseModel): 
    id: uuid.UUID
    name: str 
    email: str
    password: str 
    verify_code: int  
    role: UserRole
    is_verify: bool  

class UserRegistration(BaseModel): 
    role: UserRole
    email: str 
    name: str 
    password: str 

class UserLogin(BaseModel): 
    email: str 
    password: str