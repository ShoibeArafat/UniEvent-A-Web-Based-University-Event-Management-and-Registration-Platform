from datetime import datetime
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


def auto_migrate_schema():
    """Ensures newly added columns (such as creator_id) exist on existing tables."""
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
        if db.query(User).count() == 0:
            demo_admin = User(
                name="System Administrator",
                email="admin1@unievent.edu",
                hashed_password=auth_utils.hash_password("Admin@12345"),
                role="Admin",
                is_banned=False,
            )
            demo_organizer = User(
                name="Event Organizer",
                email="organizer@unievent.edu",
                hashed_password=auth_utils.hash_password("User@12345"),
                role="User",
                is_banned=False,
            )
            demo_student = User(
                name="Shoibe Arafat",
                email="student@unievent.edu",
                hashed_password=auth_utils.hash_password("User@12345"),
                role="User",
                is_banned=False,
            )
            db.add_all([demo_admin, demo_organizer, demo_student])
            db.commit()

        # Seed sample events if empty
        if db.query(Event).count() == 0:
            default_creator = db.query(User).filter(User.email == "organizer@unievent.edu").first()
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
