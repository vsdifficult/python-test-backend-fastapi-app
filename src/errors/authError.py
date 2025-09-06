class AuthError(Exception):
    """Базовое исключение для ошибок авторизации."""


class UserAlreadyExistsError(AuthError):
    pass


class UserNotFoundError(AuthError):
    pass


class InvalidPasswordError(AuthError):
    pass


class InvalidVerificationCodeError(AuthError):
    pass


class TokenExpiredError(AuthError):
    pass
