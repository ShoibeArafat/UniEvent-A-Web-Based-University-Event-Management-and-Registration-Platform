import sys
from pathlib import Path
from typing import Optional, List

backend_root = Path(__file__).resolve().parent.parent
if str(backend_root) not in sys.path:
    sys.path.insert(0, str(backend_root))

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database import get_db
from models import Event
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
    db_event = Event(
        title=event_in.title.strip(),
        description=event_in.description.strip(),
        location=event_in.location.strip(),
        event_date=event_in.event_date.strip(),
        organizer=event_in.organizer.strip(),
        category=event_in.category.strip(),
        capacity=event_in.capacity,
        status=event_in.status.strip() if event_in.status else "Upcoming",
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


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
    query = db.query(Event)

    if category and category.lower() != "all":
        query = query.filter(Event.category.ilike(f"%{category.strip()}%"))

    if search and search.strip():
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Event.title.ilike(term),
                Event.description.ilike(term),
                Event.organizer.ilike(term),
                Event.location.ilike(term),
            )
        )

    # Order by event_date ascending
    events = query.order_by(Event.event_date.asc(), Event.id.desc()).all()
    return events


@router.get(
    "/{event_id}",
    response_model=EventResponse,
    summary="Get a single event by ID",
    description="Retrieves full details for a specific university event by its numeric primary key.",
)
def get_single_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
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
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {event_id} not found",
        )

    update_data = event_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            if isinstance(value, str):
                setattr(event, field, value.strip())
            else:
                setattr(event, field, value)

    db.commit()
    db.refresh(event)
    return event


@router.delete(
    "/{event_id}",
    response_model=MessageResponse,
    summary="Delete an event",
    description="Removes a university event permanently from the database.",
)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {event_id} not found",
        )

    event_title = event.title
    db.delete(event)
    db.commit()
    return MessageResponse(
        message=f"Event '{event_title}' (ID {event_id}) was deleted successfully.",
        id=event_id,
    )
