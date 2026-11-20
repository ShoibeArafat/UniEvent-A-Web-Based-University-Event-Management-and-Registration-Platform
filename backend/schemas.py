from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


# ==========================================
# Event Schemas
# ==========================================

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
    creator_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str
    id: Optional[int] = None


# ==========================================
# Authentication & User Schemas
# ==========================================

class UserRegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="User full name")
    email: str = Field(..., min_length=5, max_length=255, description="Valid university or personal email")
    password: str = Field(..., min_length=6, max_length=100, description="Account password (min 6 characters)")


class UserLoginRequest(BaseModel):
    email: str = Field(..., description="Registered email address")
    password: str = Field(..., description="Account password")


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_banned: bool = False
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., description="Active refresh token string")


class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LogoutRequest(BaseModel):
    refresh_token: str = Field(..., description="Refresh token to revoke on logout")


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(..., description="Existing account password")
    new_password: str = Field(..., min_length=6, max_length=100, description="New password (min 6 characters)")


class UserProfileUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)


class UserSessionResponse(BaseModel):
    id: int
    user_agent: Optional[str] = None
    expires_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
