import sys
from pathlib import Path
from typing import Optional, List

backend_root = Path(__file__).resolve().parent.parent
if str(backend_root) not in sys.path:
    sys.path.insert(0, str(backend_root))

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database import get_db
import crud
from schemas import EventCreate, EventUpdate, EventResponse, MessageResponse

router = APIRouter(prefix="/api/events", tags=["events"])


@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new university event",
    description="Adds a new event record with validated fields (title, date, venue, category, organizer).",
)
def create_event(event_in: EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db=db, event_in=event_in)


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
    description="Updates one or more fields of an event record by ID.",
)
def update_event(event_id: int, event_in: EventUpdate, db: Session = Depends(get_db)):
    event = crud.get_event_by_id(db=db, event_id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {event_id} not found",
        )
    return crud.update_event(db=db, db_event=event, event_in=event_in)


@router.delete(
    "/{event_id}",
    response_model=MessageResponse,
    summary="Delete an event",
    description="Removes a university event permanently from the database.",
)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = crud.get_event_by_id(db=db, event_id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {event_id} not found",
        )

    event_title = event.title
    crud.delete_event(db=db, db_event=event)
    return MessageResponse(
        message=f"Event '{event_title}' (ID {event_id}) was deleted successfully.",
        id=event_id,
    )
