from datetime import datetime
from typing import Optional, List
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
    creator_name: Optional[str] = None
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
    ban_reason: Optional[str] = None
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


# ==========================================
# Event Organizing Team Schemas (Part 4)
# ==========================================

class TeamMemberAddRequest(BaseModel):
    email: EmailStr = Field(..., description="University email address of user to invite")
    role: str = Field(default="Editor", description="Role: Editor, Coordinator, Viewer")


class TeamMemberUpdateRequest(BaseModel):
    role: str = Field(..., description="Updated role: Owner, Editor, Coordinator, Viewer")


class TeamMemberResponse(BaseModel):
    id: int
    user_id: int
    user_name: str
    user_email: str
    role: str
    joined_at: datetime

    class Config:
        from_attributes = True


class EventTeamResponse(BaseModel):
    id: int
    event_id: int
    name: str
    created_at: datetime
    members: List[TeamMemberResponse] = []

    class Config:
        from_attributes = True


# ==========================================
# Admin Dashboard & Audit Log Schemas (Part 5)
# ==========================================

class AdminStatsResponse(BaseModel):
    total_users: int
    total_events: int
    total_teams: int
    active_sessions: int
    banned_users: int
    admin_count: int


class UserRoleUpdateRequest(BaseModel):
    role: str = Field(..., description="Role: Admin or User")


class UserStatusUpdateRequest(BaseModel):
    is_banned: bool = Field(..., description="True to ban user, False to activate")
    ban_reason: Optional[str] = Field(None, max_length=255, description="Reason for suspension")


class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    user_email: Optional[str] = None
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    details: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
