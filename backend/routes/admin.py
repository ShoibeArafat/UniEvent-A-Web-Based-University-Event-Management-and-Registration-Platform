"""
Admin Dashboard & Audit Logging routes (Part 5).
Strictly protected by require_admin dependency.
Provides system metrics, user management (ban/unban, role assignment),
and audit log viewing.
"""
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database import get_db
import crud_audit
from models import User, UserSession, Event, EventTeam, AuditLog
from auth_dependencies import require_admin
from schemas import (
    AdminStatsResponse,
    UserResponse,
    UserRoleUpdateRequest,
    UserStatusUpdateRequest,
    AuditLogResponse,
    MessageResponse,
)

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get(
    "/stats",
    response_model=AdminStatsResponse,
    summary="Get platform analytics and KPI metrics",
    description="Returns aggregate counts for users, events, teams, active sessions, and bans.",
)
def get_admin_stats(
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    now = datetime.utcnow()
    total_users = db.query(User).count()
    total_events = db.query(Event).count()
    total_teams = db.query(EventTeam).count()
    active_sessions = db.query(UserSession).filter(
        UserSession.is_revoked == False,
        UserSession.expires_at > now
    ).count()
    banned_users = db.query(User).filter(User.is_banned == True).count()
    admin_count = db.query(User).filter(User.role == "Admin").count()

    return AdminStatsResponse(
        total_users=total_users,
        total_events=total_events,
        total_teams=total_teams,
        active_sessions=active_sessions,
        banned_users=banned_users,
        admin_count=admin_count,
    )


@router.get(
    "/users",
    response_model=List[UserResponse],
    summary="List and search registered users",
    description="Provides user directory with filtering by search term, role, and ban status.",
)
def get_all_users(
    search: Optional[str] = Query(None, description="Search by name or email"),
    role: Optional[str] = Query(None, description="Filter by role: Admin, User"),
    status: Optional[str] = Query(None, description="Filter by status: Active, Banned"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    query = db.query(User)

    if search and search.strip():
        term = f"%{search.strip()}%"
        query = query.filter(or_(User.name.ilike(term), User.email.ilike(term)))

    if role and role.strip() and role.lower() != "all":
        query = query.filter(User.role.ilike(role.strip()))

    if status and status.strip() and status.lower() != "all":
        if status.lower() == "banned":
            query = query.filter(User.is_banned == True)
        elif status.lower() == "active":
            query = query.filter(User.is_banned == False)

    return query.order_by(User.id.asc()).all()


@router.put(
    "/users/{user_id}/status",
    response_model=UserResponse,
    summary="Ban or unban a user",
    description="Toggles user ban status. Restricted exclusively to Primary Administrator (admin1@unievent.edu).",
)
def update_user_status(
    user_id: int,
    payload: UserStatusUpdateRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    # Restrict user ban/unban access strictly to admin1@unievent.edu
    if current_admin.email != "admin1@unievent.edu":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied: Only Primary Administrator (admin1@unievent.edu) can ban or unban users.",
        )

    if user_id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Administrators cannot ban their own account.",
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.email == "admin1@unievent.edu":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Primary Administrator account cannot be banned.",
        )

    user.is_banned = payload.is_banned
    user.ban_reason = payload.ban_reason if payload.is_banned else None

    # If banned, invalidate all existing sessions immediately
    if payload.is_banned:
        db.query(UserSession).filter(UserSession.user_id == user.id).update({"is_revoked": True})

    db.commit()
    db.refresh(user)

    action_name = "USER_BAN" if payload.is_banned else "USER_UNBAN"
    crud_audit.create_audit_log(
        db=db,
        action=action_name,
        resource_type="User",
        resource_id=str(user.id),
        user_id=current_admin.id,
        details=f"{action_name} executed on {user.email}. Reason: {payload.ban_reason or 'None'}",
        ip_address=request.client.host if request.client else None,
    )

    return user


@router.put(
    "/users/{user_id}/role",
    response_model=UserResponse,
    summary="Change user role (Admin / User)",
    description="Promotes or demotes an account. System administrator only.",
)
def update_user_role(
    user_id: int,
    payload: UserRoleUpdateRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    if user_id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Administrators cannot change their own administrative role.",
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    target_role = payload.role.strip().capitalize()
    if target_role not in ["Admin", "User"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role must be 'Admin' or 'User'")

    old_role = user.role
    user.role = target_role
    db.commit()
    db.refresh(user)

    crud_audit.create_audit_log(
        db=db,
        action="USER_ROLE_CHANGE",
        resource_type="User",
        resource_id=str(user.id),
        user_id=current_admin.id,
        details=f"Changed {user.email} role from '{old_role}' to '{target_role}'",
        ip_address=request.client.host if request.client else None,
    )

    return user


@router.get(
    "/audit-logs",
    response_model=List[AuditLogResponse],
    summary="View system audit trail logs",
    description="Returns chronological audit logs with user, action, and details.",
)
def get_audit_logs(
    limit: int = Query(50, ge=1, le=200),
    action: Optional[str] = Query(None, description="Filter by action name"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    logs = crud_audit.get_audit_logs(db, limit=limit, action=action)
    return [
        AuditLogResponse(
            id=log.id,
            user_id=log.user_id,
            user_email=log.user.email if log.user else "System",
            action=log.action,
            resource_type=log.resource_type,
            resource_id=log.resource_id,
            details=log.details,
            ip_address=log.ip_address,
            created_at=log.created_at,
        )
        for log in logs
    ]
