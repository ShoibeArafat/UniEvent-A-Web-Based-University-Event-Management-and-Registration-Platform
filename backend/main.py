import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path

# Ensure backend directory is in Python path for all imports
BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import engine, Base
from models import seed_initial_events
from routes.events import router as events_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all database tables on startup
    Base.metadata.create_all(bind=engine)
    # Seed sample events if database is empty
    seed_initial_events()
    yield


app = FastAPI(
    title="UniEvent API — University Event Management Platform",
    description="REST API for CSE309 Mid Project Assessment MVP: Event Management CRUD",
    version="1.0.0",
    lifespan=lifespan,
)

# Enable CORS for local development and Vercel deployments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Event CRUD Router
app.include_router(events_router)


# Health check endpoint
@app.get("/api/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "app": "UniEvent", "version": "1.0.0"}


@app.get("/api/hello", tags=["system"])
def hello(name: str = "World") -> dict[str, str]:
    return {"message": f"Hello, {name}!"}


# Mount frontend dist when built for production / static hosting
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"

if FRONTEND_DIR.is_dir():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
