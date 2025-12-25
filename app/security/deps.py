from typing import Annotated
from fastapi import Depends, HTTPException, status, Request
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.user import User
from app.security.jwt import decode_access_token
from app.services.user_service import UserService

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(
    request: Request, db: Annotated[AsyncSession, Depends(get_session)]
) -> User:
    """
    Dependency to get the current authenticated user.
    Reads token from HttpOnly cookie, validates it, and fetches user from DB.
    """
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

    user_service = UserService(db)
    user = await user_service.get_by_email(email=email)

    if user is None:
        raise credentials_exception

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
