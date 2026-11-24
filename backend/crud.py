"""
CRUD and database operations for Event entities.
Separates data access and persistence logic from API route handlers.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from models import Event
from schemas import EventCreate, EventUpdate


def get_events(
    db: Session,
    category: Optional[str] = None,
    search: Optional[str] = None,
) -> List[Event]:
    """Retrieve all events with optional category and search filters, ordered by date."""
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

    return query.order_by(Event.event_date.asc(), Event.id.desc()).all()


def get_event_by_id(db: Session, event_id: int) -> Optional[Event]:
    """Retrieve a single event by its primary key ID."""
    return db.query(Event).filter(Event.id == event_id).first()


def create_event(
    db: Session,
    event_in: EventCreate,
    creator_id: Optional[int] = None,
) -> Event:
    """Create and persist a new event record with optional creator ownership."""
    db_event = Event(
        creator_id=creator_id,
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


def update_event(db: Session, db_event: Event, event_in: EventUpdate) -> Event:
    """Update fields on an existing event record."""
    update_data = event_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            if isinstance(value, str):
                setattr(db_event, field, value.strip())
            else:
                setattr(db_event, field, value)

    db.commit()
    db.refresh(db_event)
    return db_event


def delete_event(db: Session, db_event: Event) -> None:
    """Delete an event record permanently from the database."""
    db.delete(db_event)
    db.commit()
