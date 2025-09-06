import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from src.models.enums import UserRole
from src.database import Base
from datetime import datetime

class UserEntity(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default=UserRole.USER.value, nullable=False)
    code = Column(Integer, nullable=True)
    code_expire = Column(DateTime, nullable=True)


class RefreshTokenEntity(Base):
    __tablename__ = "refresh_tokens"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, nullable=False)
    expire_at = Column(DateTime, nullable=False)

    user = relationship("UserEntity")
