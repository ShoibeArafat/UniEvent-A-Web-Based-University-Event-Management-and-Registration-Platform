# UniEvent — University Event Management & Registration Platform

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React%2019%20(TypeScript)-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Bundler-Vite%208-646CFF?logo=vite&logoColor=white)](https://vitejs.dev)
[![Vercel](https://img.shields.io/badge/Deployment-Vercel-000000?logo=vercel&logoColor=white)](https://vercel.com)

A web-based university event management platform built for **CSE309: Web Development (Mid Project MVP)**.

---

## 🎯 MVP Feature: Event Management CRUD

For the Mid-Term 30-mark assessment, this project implements a complete, end-to-end **Event Management** feature with all 5 CRUD operations integrated across React frontend, FastAPI backend, and SQLite/Supabase database:

1. **Create:** Add a new university event with validation (title, description, venue, date, organizer, category, capacity, status).
2. **Read Single:** Inspect the detailed view of a specific event via `GET /api/events/{id}`.
3. **Read List:** Browse all events in responsive cards, with live search and category filtering ("Technology", "Competition", "Workshop", "Cultural", "Seminar").
4. **Update:** Edit any existing event's details via `PUT /api/events/{id}` with pre-populated form inputs.
5. **Delete:** Remove an event via `DELETE /api/events/{id}` with a confirmation modal and feedback alert.

---

## 📊 Mark Distribution (30 Marks Total)

| Component | Marks | Status |
|---|:---:|---|
| **Frontend Implementation** (React + TypeScript CRUD, Modals, Search/Filter, Responsive UI) | **10** | Complete |
| **Backend Implementation** (FastAPI REST API, Pydantic schemas, SQLAlchemy ORM, SQLite/Supabase) | **10** | Complete |
| **GitHub Presentation** (Issue, Feature Branch, Conventional Commits, PR Workflow) | **10** | Documented |
| **Total** | **30** | Ready for Viva |

---

## 🚀 Quickstart: Running Locally

### Prerequisites
- **Python 3.10+**
- **Node.js 20+** or **Node.js 22+**

---

### Step 1: Run Backend (FastAPI)

In a new terminal:

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1       # On Linux/macOS: source .venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt

# Run the FastAPI server
fastapi dev main.py
```

- Backend server: **http://localhost:8000**
- Interactive Swagger UI: **http://localhost:8000/docs**
- ReDoc Documentation: **http://localhost:8000/redoc**

*Note: On first startup, the server automatically initializes `events.db` and seeds sample university events.*

---

### Step 2: Run Frontend (React + TypeScript)

In a second terminal:

```bash
cd frontend

# Install frontend dependencies
npm install

# Start Vite development server
npm run dev
```

- Frontend application: **http://localhost:5173**
- Vite automatically proxies `/api/*` calls to the backend running at `http://localhost:8000`.

---

## 🌐 REST API Endpoints Specification

| Method | Endpoint | Description | Status Code |
|---|---|---|:---:|
| `POST` | `/api/events` | Create a new event record | `201 Created` |
| `GET` | `/api/events` | List all events (supports `?category=...&search=...`) | `200 OK` |
| `GET` | `/api/events/{id}` | Read full details for a single event | `200 OK` (or `404`) |
| `PUT` | `/api/events/{id}` | Update existing event record | `200 OK` (or `404`) |
| `DELETE` | `/api/events/{id}` | Permanently delete an event record | `200 OK` (or `404`) |
| `GET` | `/api/health` | Health check endpoint | `200 OK` |

---

## 🗄️ Database Model (`Event`)

The database table `events` is defined using SQLAlchemy ORM:

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto-increment | Unique identifier |
| `title` | String(200) | Not Null, Indexed | Event name |
| `description` | Text | Not Null | Detailed event description |
| `location` | String(200) | Not Null | Venue / Auditorium / Lab |
| `event_date` | String(50) | Not Null | Scheduled date (YYYY-MM-DD) |
| `organizer` | String(150) | Not Null | Department / Club / Committee |
| `category` | String(100) | Not Null, Indexed | Technology, Workshop, etc. |
| `capacity` | Integer | Default: 100 | Maximum attendee capacity |
| `status` | String(50) | Default: "Upcoming" | Upcoming / Ongoing / Completed / Cancelled |
| `created_at` | DateTime | Default: `utcnow` | Creation timestamp |
| `updated_at` | DateTime | Auto-updated on modify | Modification timestamp |

*Database configuration:* By default uses local SQLite (`backend/events.db`). If `DATABASE_URL` is set in the environment, it seamlessly connects to PostgreSQL / Supabase.

---

## 🧪 Viva Preparation Guides

Complete guides are provided in the `docs/` folder:
- 📖 **[Viva & Feature Demonstration Guide](docs/VIVA_AND_DEMO_GUIDE.md)**: Answers and walkthroughs for all 5 viva questions (CRUD demo, DevTools Network tab, REST API, Postman testing, Database models).
- 🐙 **[GitHub Presentation & PR Guide](docs/GITHUB_WORKFLOW_GUIDE.md)**: Exact issue titles, branch names, commit messages, and PR templates for maximum marks.

---

## ☁️ Deploying to Vercel

The project root includes `vercel.json` configured with two services:
1. `backend`: FastAPI service mapped to `/api/*`.
2. `frontend`: Vite static service mapped to `/*`.

To deploy:
1. Connect this repository on [Vercel](https://vercel.com/new).
2. Set Root Directory to `./`.
3. Click **Deploy**. Both services will build and deploy under one shared domain!
