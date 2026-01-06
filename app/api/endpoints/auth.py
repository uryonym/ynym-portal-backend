"""認証関連エンドポイント."""

import secrets
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from urllib.parse import urlencode

from app.database import get_session
from app.config import settings
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


def generate_state() -> str:
    return secrets.token_urlsafe(32)


@router.get("/google/login")
async def google_login(request: Request):
    """Initiate Google OAuth2 authentication flow"""
    state = generate_state()
    redirect_uri = f"{settings.backend_url}/api/auth/google/callback"

    print(f"DEBUG: Authorization redirect_uri: {redirect_uri}")

    params = {
        "response_type": "code",
        "client_id": settings.google_client_id,
        "redirect_uri": redirect_uri,
        "scope": "openid email profile",
        "state": state,
        "access_type": "offline",
        "prompt": "select_account",
    }

    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    )

    response = RedirectResponse(url=google_auth_url)
    response.set_cookie(
        key="oauth_state",
        value=state,
        httponly=True,
        max_age=600,
        secure=settings.environment == "production",
        samesite="lax",
    )
    return response


@router.get("/google/callback")
async def google_callback(
    request: Request, code: str, state: str, db: AsyncSession = Depends(get_session)
):
    """Handle the callback from Google after user consent"""
    stored_state = request.cookies.get("oauth_state")
    if not stored_state or stored_state != state:
        raise HTTPException(
            status_code=400, detail="Invalid state parameter - possible CSRF attack"
        )

    try:
        jwt_token = await auth_service.authenticate_google_user(code=code, db=db)
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR: Authentication failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")

    # Redirect to frontend dashboard with secure cookie
    response = RedirectResponse(url=f"{settings.frontend_url}")

    cookie_params = {
        "key": "access_token",
        "value": jwt_token,
        "httponly": True,
        "max_age": 60 * settings.jwt_expire_minutes,
        "secure": settings.environment == "production",
        "samesite": "lax",
        "path": "/",
    }

    # 開発環境のみlocalhostのdomainを設定
    if settings.environment == "development":
        cookie_params["domain"] = "localhost"

    response.set_cookie(**cookie_params)

    # ---  Clean up CSRF cookie ---
    response.delete_cookie("oauth_state")
    return response


@router.post("/logout")
async def logout():
    """Log out user by clearing their session cookie"""
    response = JSONResponse(content={"message": "Successfully logged out"})

    delete_params = {
        "key": "access_token",
        "httponly": True,
        "samesite": "lax",
        "path": "/",
    }

    # 開発環境のみlocalhostのdomainを設定
    if settings.environment == "development":
        delete_params["domain"] = "localhost"

    response.delete_cookie(**delete_params)
    return response
