import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Determine Database URL
# If DATABASE_URL is set (e.g. Supabase / PostgreSQL), use it.
# Otherwise fall back to a local SQLite database.
raw_db_url = os.getenv("DATABASE_URL")

if raw_db_url:
    # SQLAlchemy requires postgresql:// instead of postgres://
    if raw_db_url.startswith("postgres://"):
        raw_db_url = raw_db_url.replace("postgres://", "postgresql://", 1)
    DATABASE_URL = raw_db_url
    engine = create_engine(DATABASE_URL)
else:
    # If running on Vercel serverless environment, write SQLite to /tmp
    if os.getenv("VERCEL"):
        db_path = Path("/tmp/events.db")
    else:
        db_path = Path(__file__).resolve().parent / "events.db"
    
    DATABASE_URL = f"sqlite:///{db_path}"
    # SQLite requires check_same_thread=False for multithreaded FastAPI requests
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency that provides an active database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
