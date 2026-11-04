from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base, SessionLocal


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
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


def seed_initial_events():
    """Seeds the database with representative university events if table is empty."""
    db = SessionLocal()
    try:
        count = db.query(Event).count()
        if count == 0:
            sample_events = [
                Event(
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
