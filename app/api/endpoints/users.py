"""ユーザー関連エンドポイント."""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserResponse
from app.security.jwt import decode_access_token
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


def _get_user_service(db: Session = Depends(get_session)) -> UserService:
    return UserService(UserRepository(db))


@router.get("/me", response_model=UserResponse)
def get_current_user_me(
    request: Request,
    service: UserService = Depends(_get_user_service),
) -> UserResponse:
    """現在のログインユーザー情報を取得."""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = decode_access_token(token)
        user_email = payload.get("sub")
        if not user_email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        user = service.get_by_email(email=user_email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
