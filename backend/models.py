from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, text
from sqlalchemy.orm import relationship
from database import Base, SessionLocal, engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="User", nullable=False)  # "User" or "Admin"
    is_banned = Column(Boolean, default=False, nullable=False)
    ban_reason = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="creator")
    team_memberships = relationship("TeamMember", back_populates="user", cascade="all, delete-orphan")


class UserSession(Base):
    """
    Session table to manage revocable JWT refresh tokens.
    Stores the SHA-256 hash of the token rather than the raw token string.
    """
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash = Column(String(64), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)
    user_agent = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="sessions")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    location = Column(String(200), nullable=False)
    event_date = Column(String(50), nullable=False)
    organizer = Column(String(150), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    capacity = Column(Integer, default=100, nullable=False)
    status = Column(String(50), default="Upcoming", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    creator = relationship("User", back_populates="events")
    team = relationship("EventTeam", back_populates="event", uselist=False, cascade="all, delete-orphan")

    @property
    def creator_name(self) -> Optional[str]:
        return self.creator.name if self.creator else None


class EventTeam(Base):
    """
    Organizing team for an event.
    Linked 1-to-1 with an Event.
    """
    __tablename__ = "event_teams"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    name = Column(String(150), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    event = relationship("Event", back_populates="team")
    members = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")


class TeamMember(Base):
    """
    Member of an organizing team with specific permission tier:
    Owner, Editor, Coordinator, Viewer.
    """
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey("event_teams.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(50), default="Editor", nullable=False)  # "Owner", "Editor", "Coordinator", "Viewer"
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    team = relationship("EventTeam", back_populates="members")
    user = relationship("User", back_populates="team_memberships")


class AuditLog(Base):
    """
    Administrative and security audit trail.
    Tracks critical system actions (logins, creates, updates, deletes, bans, role changes).
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(String(50), nullable=True)
    details = Column(Text, nullable=True)
    ip_address = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User")


def auto_migrate_schema():
    """Ensures newly added tables and columns (such as creator_id, event_teams, audit_logs) exist."""
    Base.metadata.create_all(bind=engine)
    with engine.begin() as conn:
        try:
            # Check SQLite table info
            result = conn.execute(text("PRAGMA table_info(events)"))
            columns = [row[1] for row in result.fetchall()]
            if columns and "creator_id" not in columns:
                conn.execute(text("ALTER TABLE events ADD COLUMN creator_id INTEGER"))
        except Exception:
            # If not SQLite, try PostgreSQL ALTER TABLE ADD COLUMN IF NOT EXISTS
            try:
                conn.execute(text("ALTER TABLE events ADD COLUMN IF NOT EXISTS creator_id INTEGER"))
            except Exception:
                pass


def seed_initial_events():
    """Seeds the database with representative university events and demo users if empty."""
    import auth_utils
    auto_migrate_schema()
    db = SessionLocal()
    try:
        # Seed demo users if empty
        # Seed or ensure all 5 demo accounts exist (for teacher viva)
        demo_accounts = [
            {
                "name": "System Administrator",
                "email": "admin1@unievent.edu",
                "password": "Admin@12345",
                "role": "Admin",
            },
            {
                "name": "Secondary Administrator",
                "email": "admin2@unievent.edu",
                "password": "Admin@12345",
                "role": "Admin",
            },
            {
                "name": "Shoibe Arafat",
                "email": "student@unievent.edu",
                "password": "User@12345",
                "role": "User",
            },
            {
                "name": "Tanvir Ahmed",
                "email": "student2@unievent.edu",
                "password": "Tanvir#2026!",
                "role": "User",
            },
            {
                "name": "Nafis Fuad",
                "email": "student3@unievent.edu",
                "password": "Nafis@Pass99",
                "role": "User",
            },
            {
                "name": "Sadia Rahman",
                "email": "student4@unievent.edu",
                "password": "Sadia*Secure1",
                "role": "User",
            },
            {
                "name": "Farhan Kabir",
                "email": "student5@unievent.edu",
                "password": "Farhan#Key2026",
                "role": "User",
            },
        ]

        for acc in demo_accounts:
            existing_user = db.query(User).filter(User.email == acc["email"]).first()
            if not existing_user:
                new_user = User(
                    name=acc["name"],
                    email=acc["email"],
                    hashed_password=auth_utils.hash_password(acc["password"]),
                    role=acc["role"],
                    is_banned=False,
                )
                db.add(new_user)
        db.commit()

        # Seed sample events if empty
        if db.query(Event).count() == 0:
            default_creator = db.query(User).filter(User.email == "student@unievent.edu").first()
            creator_id = default_creator.id if default_creator else None

            sample_events = [
                Event(
                    creator_id=creator_id,
                    title="Tech Fest 2026",
                    description="Annual university flagship technology festival featuring competitive robotics, project exhibitions, and AI keynote lectures.",
                    location="Main Campus Auditorium & Plaza",
                    event_date="2026-11-20",
                    organizer="CSE Department",
                    category="Technology",
                    capacity=350,
                    status="Upcoming",
                ),
                Event(
                    creator_id=creator_id,
                    title="Inter-University Programming Contest",
                    description="Collegiate competitive programming contest bringing together top problem solvers to solve algorithmic challenges under ICPC rules.",
                    location="Central Computer Lab 3 & 4",
                    event_date="2026-11-25",
                    organizer="ACM Student Chapter",
                    category="Competition",
                    capacity=120,
                    status="Upcoming",
                ),
                Event(
                    creator_id=creator_id,
                    title="Hands-on Robotics & IoT Workshop",
                    description="Practical workshop covering microcontroller interfacing with ESP32, sensor integration, motor control, and MQTT telemetry.",
                    location="Engineering Building Lab B",
                    event_date="2026-11-28",
                    organizer="Robotics Club",
                    category="Workshop",
                    capacity=60,
                    status="Upcoming",
                ),
                Event(
                    creator_id=creator_id,
                    title="University Cultural Gala & Concert",
                    description="A vibrant evening of musical ensembles, traditional dance, theatrical skits, and cultural performances by student artists.",
                    location="University Open-Air Amphitheatre",
                    event_date="2026-12-05",
                    organizer="Cultural Affairs Society",
                    category="Cultural",
                    capacity=500,
                    status="Upcoming",
                ),
                Event(
                    creator_id=creator_id,
                    title="AI & Modern Web Development Seminar",
                    description="Distinguished guest session on building full-stack web applications using FastAPI, React TypeScript, and machine learning APIs.",
                    location="Seminar Room 204",
                    event_date="2026-12-10",
                    organizer="IEEE Student Branch",
                    category="Seminar",
                    capacity=80,
                    status="Upcoming",
                ),
            ]
            db.add_all(sample_events)
            db.commit()
    finally:
        db.close()
