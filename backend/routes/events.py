import sys
from pathlib import Path
from typing import Optional, List

backend_root = Path(__file__).resolve().parent.parent
if str(backend_root) not in sys.path:
    sys.path.insert(0, str(backend_root))

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from database import get_db
import crud
import crud_teams
import crud_audit
from models import User
from auth_dependencies import get_current_user
from schemas import EventCreate, EventUpdate, EventResponse, MessageResponse

router = APIRouter(prefix="/api/events", tags=["events"])


@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new university event",
    description="Adds a new event record linked to the authenticated user.",
)
def create_event(
    event_in: EventCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    event = crud.create_event(db=db, event_in=event_in, creator_id=current_user.id)
    crud_teams.get_or_create_event_team(db, event=event)
    crud_audit.create_audit_log(
        db=db,
        action="EVENT_CREATE",
        resource_type="Event",
        resource_id=str(event.id),
        user_id=current_user.id,
        details=f"Created event '{event.title}' in category '{event.category}'",
        ip_address=request.client.host if request.client else None,
    )
    return event


@router.get(
    "",
    response_model=List[EventResponse],
    summary="List all events",
    description="Retrieves a list of all university events with optional search and category filters.",
)
def get_events(
    category: Optional[str] = Query(None, description="Filter by event category"),
    search: Optional[str] = Query(None, description="Search term for title, description, or organizer"),
    db: Session = Depends(get_db),
):
    return crud.get_events(db=db, category=category, search=search)


@router.get(
    "/{event_id}",
    response_model=EventResponse,
    summary="Get a single event by ID",
    description="Retrieves full details for a specific university event by its numeric primary key.",
)
def get_single_event(event_id: int, db: Session = Depends(get_db)):
    event = crud.get_event_by_id(db=db, event_id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {event_id} not found",
        )
    return event


@router.put(
    "/{event_id}",
    response_model=EventResponse,
    summary="Update an existing event",
    description="Updates an event record by ID. Creator, Editor team members, or Admins only.",
)
def update_event(
    event_id: int,
    event_in: EventUpdate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    event = crud.get_event_by_id(db=db, event_id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {event_id} not found",
        )

    # RBAC: Creator, team Editor/Owner, or Admin
    if not crud_teams.user_can_edit_event(db, event=event, user=current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied: You do not have permission to edit this event. Only the creator, team editors, or an Admin can modify it.",
        )

    updated = crud.update_event(db=db, db_event=event, event_in=event_in)
    crud_audit.create_audit_log(
        db=db,
        action="EVENT_UPDATE",
        resource_type="Event",
        resource_id=str(event.id),
        user_id=current_user.id,
        details=f"Updated event '{updated.title}'",
        ip_address=request.client.host if request.client else None,
    )
    return updated


@router.delete(
    "/{event_id}",
    response_model=MessageResponse,
    summary="Delete an event",
    description="Removes an event permanently. Creator or Admin only.",
)
def delete_event(
    event_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    event = crud.get_event_by_id(db=db, event_id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {event_id} not found",
        )

    # RBAC: Deletion is strictly reserved for Admin or primary Creator
    is_admin = current_user.role == "Admin"
    is_owner = event.creator_id is not None and event.creator_id == current_user.id
    if not is_admin and not is_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied: Only the original event creator or an Admin can delete this event.",
        )

    event_title = event.title
    crud.delete_event(db=db, db_event=event)
    crud_audit.create_audit_log(
        db=db,
        action="EVENT_DELETE",
        resource_type="Event",
        resource_id=str(event_id),
        user_id=current_user.id,
        details=f"Deleted event '{event_title}' (ID: {event_id})",
        ip_address=request.client.host if request.client else None,
    )
    return MessageResponse(
        message=f"Event '{event_title}' (ID {event_id}) was deleted successfully.",
        id=event_id,
    )
