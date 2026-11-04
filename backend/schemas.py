from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class EventBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=200, description="Title of the event")
    description: str = Field(..., min_length=5, description="Detailed description of the event")
    location: str = Field(..., min_length=2, max_length=200, description="Venue or room location")
    event_date: str = Field(..., min_length=4, max_length=50, description="Event date (e.g. YYYY-MM-DD)")
    organizer: str = Field(..., min_length=2, max_length=150, description="Organizing body or department")
    category: str = Field(..., min_length=2, max_length=100, description="Category (Technology, Competition, Workshop, Cultural, Seminar)")
    capacity: int = Field(default=100, ge=1, le=10000, description="Maximum participant capacity")
    status: str = Field(default="Upcoming", max_length=50, description="Event status: Upcoming, Ongoing, Completed, or Cancelled")


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=200)
    description: Optional[str] = Field(None, min_length=5)
    location: Optional[str] = Field(None, min_length=2, max_length=200)
    event_date: Optional[str] = Field(None, min_length=4, max_length=50)
    organizer: Optional[str] = Field(None, min_length=2, max_length=150)
    category: Optional[str] = Field(None, min_length=2, max_length=100)
    capacity: Optional[int] = Field(None, ge=1, le=10000)
    status: Optional[str] = Field(None, max_length=50)


class EventResponse(EventBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str
    id: Optional[int] = None
