from fastapi import HTTPException, Request, status
from passlib.context import CryptContext  # type: ignore[import-untyped]
from sqladmin.authentication import AuthenticationBackend

from libs.repositories.admin_user_repository import get_admin_user_by_email

pwd_ctx = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def require_admin_session(request: Request) -> None:
    if "user" in request.session:
        return
    raise HTTPException(
        status_code=status.HTTP_302_FOUND,
        headers={"Location": "/admin/login"},
        detail="Admin authentication required",
    )


class AdminAuth(AuthenticationBackend):
    async def login(self, request) -> bool:
        form = await request.form()
        email = (form.get("username") or "").lower().strip()
        password = form.get("password") or ""

        admin_user = await get_admin_user_by_email(email)
        if admin_user and pwd_ctx.verify(password, admin_user.hashed_password):
            request.session.update({"user": email})
            return True

        return False

    async def logout(self, request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request) -> bool:
        return "user" in request.session
