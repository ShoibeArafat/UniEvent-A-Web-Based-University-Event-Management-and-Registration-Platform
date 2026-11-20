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
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from database import engine, Base
from models import seed_initial_events
from routes.events import router as events_router
from routes.auth import router as auth_router
from routes.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all database tables on startup (users, user_sessions, events)
    Base.metadata.create_all(bind=engine)
    # Seed sample events and demo users if database is empty
    seed_initial_events()
    yield


app = FastAPI(
    title="UniEvent API — University Event Management Platform",
    description="REST API for CSE309 University Event Management Platform with JWT Authentication, Revocable Sessions, and Event Management CRUD",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# Convenience redirects for root paths
@app.get("/docs", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url="/api/docs")


@app.get("/redoc", include_in_schema=False)
def redoc_redirect():
    return RedirectResponse(url="/api/redoc")


@app.get("/openapi.json", include_in_schema=False)
def openapi_redirect():
    return RedirectResponse(url="/api/openapi.json")


# Enable CORS for local development and Vercel deployments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_router)
app.include_router(users_router)
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
