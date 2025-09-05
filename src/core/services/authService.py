import uuid
import bcrypt
import jwt
from datetime import datetime, timedelta

from src.repositories.user_repository import UserRepository
from src.models.dto.UserDto import UserDto, UserLogin, UserRegistration
from src.models.dto.AuthDto import AuthModel, UserRole


SECRET_KEY = "super_secret_key"   
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


class AuthService:
    def __init__(self, session):
        self.user_repository = UserRepository()
        self.session = session   

    async def sign_up(self, user_body: UserRegistration) -> AuthModel:
        """
        Регистрация нового пользователя.
        """
        existing_user = await self.user_repository.get_by_email(self.session, user_body.email)
        if existing_user:
            raise ValueError("User with this email already exists")

        hashed_password = bcrypt.hashpw(user_body.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        user_dto = UserDto(
            id=uuid.uuid4(),
            email=user_body.email,
            username=user_body.username,
            password_hash=hashed_password,
            role=UserRole.USER
        )

        created_user = await self.user_repository.create_async(self.session, user_dto)

        access_token = self._create_token(created_user.id, created_user.role, ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token = self._create_token(created_user.id, created_user.role, REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60)

        return AuthModel(
            success=True,
            user_id=created_user.id,
            role=created_user.role,
            access_token=access_token,
            refresh_token=refresh_token
        )

    async def sign_in(self, user_body: UserLogin) -> AuthModel:
        """
        Авторизация пользователя.
        """
        user = await self.user_repository.get_by_email(self.session, user_body.email)
        if not user:
            raise ValueError("User not found")

        if not bcrypt.checkpw(user_body.password.encode("utf-8"), user.password_hash.encode("utf-8")):
            raise ValueError("Invalid password")

        access_token = self._create_token(user.id, user.role, ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token = self._create_token(user.id, user.role, REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60)

        return AuthModel(
            success=True,
            user_id=user.id,
            role=user.role,
            access_token=access_token,
            refresh_token=refresh_token
        )

    async def verification_email(self, email: str, code: int) -> AuthModel:
        """
        Подтверждение email (заглушка).
        """
        user = await self.user_repository.get_by_email(self.session, email)
        if not user:
            raise ValueError("User not found")
        
        if code != 1234: 
            raise ValueError("Invalid verification code")

        access_token = self._create_token(user.id, user.role, ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token = self._create_token(user.id, user.role, REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60)

        return AuthModel(
            success=True,
            user_id=user.id,
            role=user.role,
            access_token=access_token,
            refresh_token=refresh_token
        )

    def _create_token(self, user_id: uuid.UUID, role: UserRole, expires_minutes: int) -> str:
        """
        Генерация JWT токена.
        """
        expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
        payload = {
            "sub": str(user_id),
            "role": role,
            "exp": expire
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM) 

    
