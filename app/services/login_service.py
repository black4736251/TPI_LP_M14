from dataclasses import dataclass
from typing import Self


from app.core.database import check_user, get_user
from app.models.user_model import User


@dataclass(frozen = True)
class LoginResult:
    success: bool
    error: str | None = None
    user: User | None = None
    role: str | None = None

class LoginService:
    _instance: "LoginService | None" = None

    def __new__(cls) -> Self | LoginService:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def login(self, user_name: str, password: str) -> LoginResult:
        user_name = user_name.strip()
        password = password.strip()

        if not user_name or not password:
            return LoginResult(
                success = False,
                error = "empty_fields"
            )

        if not check_user(user_name = user_name, user_password = password):
            return LoginResult(
                success = False,
                error = "invalid_credentials"
            )

        user = get_user(user_name = user_name)
        if user is None:
            return LoginResult(
                success = False,
                error = "invalid_credentials"
            )

        return LoginResult(
            success = True,
            user = user,
            role = user.user_role
        )