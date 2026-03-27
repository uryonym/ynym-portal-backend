"""認証関連エンドポイント."""

import secrets
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database import get_session
from app.repositories.user_repository import UserRepository
from app.services.auth_service import auth_service
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


def _get_user_service(db: Session = Depends(get_session)) -> UserService:
    return UserService(UserRepository(db))


def generate_state() -> str:
    return secrets.token_urlsafe(32)


@router.get("/google/login")
def google_login(request: Request):
    """Google OAuth2 認証フローを開始."""
    state = generate_state()
    redirect_uri = f"{settings.BACKEND_URL}/api/auth/google/callback"
    params = {
        "response_type": "code",
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "scope": "openid email profile",
        "state": state,
        "access_type": "offline",
        "prompt": "select_account",
    }
    google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    response = RedirectResponse(url=google_auth_url)
    response.set_cookie(
        key="oauth_state",
        value=state,
        httponly=True,
        max_age=600,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax",
    )
    return response


@router.get("/google/callback")
def google_callback(
    request: Request,
    code: str,
    state: str,
    user_service: UserService = Depends(_get_user_service),
):
    """Google コールバックを処理してJWTクッキーをセット."""
    stored_state = request.cookies.get("oauth_state")
    if not stored_state or stored_state != state:
        raise HTTPException(status_code=400, detail="Invalid state parameter - possible CSRF attack")

    try:
        jwt_token = auth_service.authenticate_google_user(code=code, user_service=user_service)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")

    response = RedirectResponse(url=f"{settings.FRONTEND_URL}")
    cookie_params = {
        "key": "access_token",
        "value": jwt_token,
        "httponly": True,
        "max_age": 60 * settings.JWT_EXPIRE_MINUTES,
        "secure": settings.ENVIRONMENT == "production",
        "samesite": "lax",
        "path": "/",
    }
    if settings.ENVIRONMENT == "development":
        cookie_params["domain"] = "localhost"
    response.set_cookie(**cookie_params)
    response.delete_cookie("oauth_state")
    return response


@router.post("/logout")
def logout():
    """ログアウト（セッションクッキーを削除）."""
    response = JSONResponse(content={"message": "Successfully logged out"})
    delete_params = {"key": "access_token", "httponly": True, "samesite": "lax", "path": "/"}
    if settings.ENVIRONMENT == "development":
        delete_params["domain"] = "localhost"
    response.delete_cookie(**delete_params)
    return response
