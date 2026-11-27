"""  Create and update user..... also user jwd session manage..
CRUD operations for User authentication, password management, and revocable sessions.
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session

from models import User, UserSession
from schemas import UserRegisterRequest
import auth_utils


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Look up a user record by normalized lowercase email."""
    return db.query(User).filter(User.email == email.strip().lower()).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Look up a user record by primary key ID."""
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user_in: UserRegisterRequest) -> User:
    """Create a new User record with a bcrypt hashed password."""
    hashed_pwd = auth_utils.hash_password(user_in.password)
    user = User(
        name=user_in.name.strip(),
        email=user_in.email.strip().lower(),
        hashed_password=hashed_pwd,
        role="User",
        is_banned=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_password(db: Session, user: User, new_hashed_password: str) -> User:
    """Updates a user's hashed password and commits to database."""
    user.hashed_password = new_hashed_password
    db.commit()
    db.refresh(user)
    return user


def update_user_profile(db: Session, user: User, name: str) -> User:
    """Updates a user's display name."""
    user.name = name.strip()
    db.commit()
    db.refresh(user)
    return user


# ==========================================
# Session & Refresh Token Operations
# ==========================================

def create_user_session(
    db: Session,
    user_id: int,
    refresh_token: str,
    user_agent: Optional[str] = None
) -> UserSession:
    """
    Records an active session in the database.
    Stores the SHA-256 hash of the token rather than the raw token string.
    """
    token_hash = auth_utils.hash_refresh_token(refresh_token)
    expires_at = auth_utils.get_refresh_token_expiration()

    session = UserSession(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at,
        is_revoked=False,
        user_agent=user_agent[:255] if user_agent else None,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_active_session_by_token(db: Session, refresh_token: str) -> Optional[UserSession]:
    """
    Looks up a session by computing the SHA-256 hash of the incoming token.
    Returns session only if it exists, is not revoked, and has not expired.
    """
    token_hash = auth_utils.hash_refresh_token(refresh_token)
    session = db.query(UserSession).filter(
        UserSession.token_hash == token_hash,
        UserSession.is_revoked == False,
        UserSession.expires_at > datetime.utcnow()
    ).first()
    return session


def revoke_session(db: Session, refresh_token: str) -> bool:
    """
    Marks a session as revoked (is_revoked = True) given its raw token.
    Used during logout to invalidate the session.
    """
    token_hash = auth_utils.hash_refresh_token(refresh_token)
    session = db.query(UserSession).filter(UserSession.token_hash == token_hash).first()
    if session:
        session.is_revoked = True
        db.commit()
        return True
    return False


def revoke_session_by_id(db: Session, session_id: int, user_id: int) -> bool:
    """Revokes a specific session belonging to the user (e.g. from session management screen)."""
    session = db.query(UserSession).filter(
        UserSession.id == session_id,
        UserSession.user_id == user_id
    ).first()
    if session:
        session.is_revoked = True
        db.commit()
        return True
    return False


def revoke_all_user_sessions(db: Session, user_id: int) -> None:
    """Revokes all active sessions for a user (e.g. on security breach or password change)."""
    db.query(UserSession).filter(
        UserSession.user_id == user_id,
        UserSession.is_revoked == False
    ).update({"is_revoked": True})
    db.commit()


def get_user_sessions(db: Session, user_id: int) -> List[UserSession]:
    """Returns active (non-revoked, non-expired) sessions for a user."""
    return db.query(UserSession).filter(
        UserSession.user_id == user_id,
        UserSession.is_revoked == False,
        UserSession.expires_at > datetime.utcnow()
    ).order_by(UserSession.created_at.desc()).all()
