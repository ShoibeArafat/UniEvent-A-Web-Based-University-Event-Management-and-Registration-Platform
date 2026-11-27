"""
Event service layer.
Provides business logic for events, delegating data access to the CRUD layer.
"""
from typing import List, Optional
from sqlalchemy.orm import Session

import crud
from schemas import EventCreate, EventUpdate
from models import Event


class EventService:
    """Service providing event operations for route handlers."""

    @staticmethod
    def get_all(
        db: Session,
        category: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[Event]:
        return crud.get_events(db=db, category=category, search=search)

    @staticmethod
    def get_by_id(db: Session, event_id: int) -> Optional[Event]:
        return crud.get_event_by_id(db=db, event_id=event_id)

    @staticmethod
    def create(db: Session, event_in: EventCreate, creator_id: Optional[int] = None) -> Event:
        return crud.create_event(db=db, event_in=event_in, creator_id=creator_id)

    @staticmethod
    def update(db: Session, db_event: Event, event_in: EventUpdate) -> Event:
        return crud.update_event(db=db, db_event=db_event, event_in=event_in)

    @staticmethod
    def delete(db: Session, db_event: Event) -> None:
        crud.delete_event(db=db, db_event=db_event)
