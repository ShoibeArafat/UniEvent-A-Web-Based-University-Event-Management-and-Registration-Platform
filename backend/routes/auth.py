""" authentication endpont...
Authentication API endpoints: Signup, Login, Token Refresh, and Logout.
"""
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    LogoutRequest,
    MessageResponse,
)
import auth_utils
import crud_auth

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post(
    "/signup",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
    description="Creates a new account, hashes password using bcrypt, and returns access + refresh tokens.",
)
def signup(
    user_in: UserRegisterRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    # Check if email is already taken
    existing_user = crud_auth.get_user_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists.",
        )

    # Create new user
    user = crud_auth.create_user(db, user_in=user_in)

    # Generate tokens
    access_token = auth_utils.create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role}
    )
    refresh_token = auth_utils.generate_refresh_token()

    # Record active session with hashed refresh token
    user_agent = request.headers.get("User-Agent", "Unknown Device")
    crud_auth.create_user_session(
        db, user_id=user.id, refresh_token=refresh_token, user_agent=user_agent
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=user,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate user and obtain JWT tokens",
    description="Validates credentials, verifies account status, and issues access + refresh tokens.",
)
def login(
    login_data: UserLoginRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    user = crud_auth.get_user_by_email(db, email=login_data.email)
    if not user or not auth_utils.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.is_banned:
        reason = user.ban_reason or "Account suspended by administrator"
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Login disabled: {reason}.",
        )

    # Issue new token pair
    access_token = auth_utils.create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role}
    )
    refresh_token = auth_utils.generate_refresh_token()

    # Store hashed refresh token in user_sessions table
    user_agent = request.headers.get("User-Agent", "Unknown Device")
    crud_auth.create_user_session(
        db, user_id=user.id, refresh_token=refresh_token, user_agent=user_agent
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=user,
    )


@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
    summary="Refresh an expired access token",
    description="Exchanges an active refresh token for a newly generated 15-minute access token.",
)
def refresh_token(
    refresh_in: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    session = crud_auth.get_active_session_by_token(db, refresh_token=refresh_in.refresh_token)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid, expired, or revoked refresh token. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = session.user
    if user.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account has been suspended.",
        )

    new_access_token = auth_utils.create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role}
    )

    return RefreshTokenResponse(
        access_token=new_access_token,
        token_type="bearer",
    )


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Revoke refresh token and log out",
    description="Invalidates the provided refresh token session in the database so it can no longer be used.",
)
def logout(
    logout_in: LogoutRequest,
    db: Session = Depends(get_db)
):
    revoked = crud_auth.revoke_session(db, refresh_token=logout_in.refresh_token)
    return MessageResponse(
        message="Logged out successfully. Session revoked." if revoked else "Session already expired or revoked."
    )
