"""認証依存性."""

from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.security.jwt import decode_access_token
from app.services.user_service import UserService

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    request: Request,
    db: Annotated[Session, Depends(get_session)],
) -> User:
    """HttpOnly クッキーから JWT を検証し、現在のユーザーを返す."""
    token = request.cookies.get("access_token")
    if token is None:
        raise credentials_exception

    try:
        payload = decode_access_token(token)
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except (JWTError, Exception):
        raise credentials_exception

    user_service = UserService(UserRepository(db))
    user = user_service.get_by_email(email=email)
    if user is None:
        raise credentials_exception

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
