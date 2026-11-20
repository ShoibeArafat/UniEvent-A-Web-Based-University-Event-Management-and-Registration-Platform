"""
User profile and session management routes.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import (
    UserResponse,
    UserProfileUpdateRequest,
    PasswordChangeRequest,
    UserSessionResponse,
    MessageResponse,
)
from auth_dependencies import get_current_user
import auth_utils
import crud_auth

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Returns authenticated user profile information based on the Bearer access token.",
)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Update current user profile",
    description="Updates the authenticated user's display name.",
)
def update_profile(
    profile_in: UserProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if profile_in.name and profile_in.name.strip():
        current_user = crud_auth.update_user_profile(
            db, user=current_user, name=profile_in.name
        )
    return current_user


@router.post(
    "/change-password",
    response_model=MessageResponse,
    summary="Change account password",
    description="Verifies the current password before setting a new bcrypt hashed password and revoking other sessions.",
)
def change_password(
    password_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not auth_utils.verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password entered is incorrect.",
        )

    new_hash = auth_utils.hash_password(password_data.new_password)
    crud_auth.update_user_password(db, user=current_user, new_hashed_password=new_hash)

    # Invalidate other active sessions for account security
    crud_auth.revoke_all_user_sessions(db, user_id=current_user.id)

    return MessageResponse(
        message="Password updated successfully. Other active sessions have been signed out."
    )


@router.get(
    "/me/sessions",
    response_model=List[UserSessionResponse],
    summary="List active sessions",
    description="Returns all active, non-expired refresh token sessions across devices for the current user.",
)
def list_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sessions = crud_auth.get_user_sessions(db, user_id=current_user.id)
    return sessions


@router.delete(
    "/me/sessions/{session_id}",
    response_model=MessageResponse,
    summary="Revoke an active session",
    description="Revokes a specific session (device) belonging to the authenticated user.",
)
def revoke_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    revoked = crud_auth.revoke_session_by_id(db, session_id=session_id, user_id=current_user.id)
    if not revoked:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or already revoked.",
        )
    return MessageResponse(message="Device session revoked successfully.")
