"""
CRUD and logging helper for AuditLog entries (Part 5).
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from models import AuditLog, User


def create_audit_log(
    db: Session,
    action: str,
    resource_type: str,
    user_id: Optional[int] = None,
    resource_id: Optional[str] = None,
    details: Optional[str] = None,
    ip_address: Optional[str] = None,
) -> AuditLog:
    """Persists a new administrative or security audit record."""
    entry = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def get_audit_logs(
    db: Session,
    limit: int = 100,
    offset: int = 0,
    action: Optional[str] = None,
) -> List[AuditLog]:
    """Retrieve audit logs ordered by newest first."""
    query = db.query(AuditLog)
    if action and action.strip():
        query = query.filter(AuditLog.action.ilike(f"%{action.strip()}%"))
    return query.order_by(AuditLog.created_at.desc()).offset(offset).limit(limit).all()
