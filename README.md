# UniEvent — University Event Management & Registration Platform

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React%2019%20(TypeScript)-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Bundler-Vite%208-646CFF?logo=vite&logoColor=white)](https://vitejs.dev)
[![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20Supabase%20PostgreSQL-336791?logo=postgresql&logoColor=white)](https://supabase.com)
[![Deployment](https://img.shields.io/badge/Deployment-Vercel-000000?logo=vercel&logoColor=white)](https://2131108.vercel.app)

A full-stack, enterprise-grade university event management platform engineered for **CSE309: Web Engineering Final Project**.

- 🌐 **Live Production Site:** [https://2131108.vercel.app](https://2131108.vercel.app)
- 📖 **Interactive Swagger UI:** [https://2131108.vercel.app/api/docs](https://2131108.vercel.app/api/docs)

---

## 🎯 System Architecture & Key Features

UniEvent is built following a clean layered architecture with a single unified database, token revocation, role-based authorization, and collaborative team permissions:

### 1. Dual-Token JWT Authentication & Session Revocation
- **Short-lived Access Tokens (15 min):** Transmitted via Bearer authorization headers.
- **Long-lived Refresh Tokens (7 days):** Stored securely and hashed using SHA-256 in the database (`user_sessions`).
- **Immediate Session Invalidation:** Logging out instantly sets `is_revoked = True` in the database, preventing token replay attacks.
- **Dedicated Login Portal:** Full-screen responsive authentication gateway with tab switching (Sign In vs Create Account) and quick demo accounts for examiners.

### 2. Event Management CRUD & RBAC Ownership
- **Complete CRUD Operations:** Create, Read (single & paginated list), Update, and Delete with input validation.
- **Event Ownership:** Events are tagged with `creator_id`. Only the creator, authorized team members, or Administrators can edit/delete events.
- **Role Badges & Dashboard Filtering:** Visual badges (`★ Your Event`, `Admin`) and dedicated `"My Events"` filter view.

### 3. Shared Organizing Teams (Collaborative Permissions)
- **1-to-1 Event Teams:** An event team is automatically provisioned whenever an event is created, setting the creator as **Owner**.
- **4 Permission Tiers:**
  - **Owner:** Full event management, team member invites, role changes, and deletion.
  - **Editor:** Can edit event schedule, capacity, and details.
  - **Coordinator:** Can view team operations and manage event logistics.
  - **Viewer:** Read-only access to team roster and event settings.
- **Two-Tab Modal:** Overview and Organizing Team tabs within `EventDetailModal`.

### 4. Administrator Center & Governance
- **KPI Overview Metrics:** Live counts of registered users, published events, collaborative teams, active sessions, and banned accounts.
- **User Directory Management:** Search, role/status filtering, role promotion (`User` ↔ `Admin`), and account ban/unban with documented reason.
- **Audit Logging System:** Comprehensive trail recording `action`, `actor_id`, `resource_type`, `resource_id`, and `details`.
- **CSV Data Export:** One-click CSV reports for both events and user rosters.

### 5. Cloud Database Integration (Supabase PostgreSQL & SQLite)
- **Automatic Fallback:** Uses local SQLite (`backend/events.db`) in local environments, and connects seamlessly to Supabase PostgreSQL when `DATABASE_URL` is set.
- **Zero-Migration Engine:** `Base.metadata.create_all()` and automated schema migration on application startup.

---

## 🔑 Demo Accounts (For Teacher Assessment & Viva)

The application seeds 5 ready-to-test accounts representing all permission levels:

| Role | University Email | Password | Permissions & Intended Test Flow |
|---|---|---|---|
| **Admin 1** | `admin1@unievent.edu` | `Admin@12345` | Primary Admin. Can access Admin Center, ban users, view audit trail, export CSV, and override any event. |
| **Admin 2** | `admin2@unievent.edu` | `Admin@12345` | Secondary Admin. Multi-admin governance testing. |
| **Student** | `student@unievent.edu` | `User@12345` | Student / Attendee (`Shoibe Arafat`). Creates personal events, tests creator permissions. |
| **Organizer** | `organizer@unievent.edu` | `User@12345` | Department organizer. Owns seeded university events (Tech Fest, ICPC Contest). |
| **Co-Editor** | `editor@unievent.edu` | `User@12345` | Team collaborator account. Used to demonstrate collaborative team editing. |

*Quick-fill demo buttons are built right into the Login screen for instant 1-click credential loading during demonstration!*

---

## 🚀 Running the Project Locally

### Prerequisites
- **Python 3.10+** (Python 3.11 recommended)
- **Node.js 20+** or **Node.js 22+**

---

### Step 1: Run Backend (FastAPI)

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

- Backend Server: **http://localhost:8000**
- Interactive Swagger UI: **http://localhost:8000/docs**
- Health Check: **http://localhost:8000/api/health**

---

### Step 2: Run Frontend (React + Vite + TypeScript)

```bash
cd frontend

# Install frontend dependencies
npm install

# Start Vite development server
npm run dev
```

- Frontend Application: **http://localhost:5173**
- Vite proxies `/api/*` requests directly to `http://localhost:8000`.

---

### Step 3: Run Automated Test Suites

```bash
cd backend
python test_auth.py          # Part 1 & 2: JWT & Token Revocation (8 tests)
python test_rbac.py          # Part 3: Ownership & RBAC (10 tests)
python test_parts_4_5.py     # Part 4 & 5: Teams, Admin & Audit (16 tests)
```

---

## 🌐 REST API Endpoints Specification

### Authentication & Sessions
| Method | Endpoint | Description | Access |
|---|---|---|:---:|
| `POST` | `/api/auth/signup` | Register new university account | Public |
| `POST` | `/api/auth/login` | Authenticate & receive access + refresh tokens | Public |
| `POST` | `/api/auth/refresh` | Exchange valid refresh token for new access token | Public |
| `POST` | `/api/auth/logout` | Revoke active refresh token session in database | Authenticated |
| `GET` | `/api/users/me` | Fetch currently authenticated user profile | Authenticated |
| `GET` | `/api/users/me/sessions` | View user's active session history | Authenticated |

### Events (CRUD & RBAC)
| Method | Endpoint | Description | Access |
|---|---|---|:---:|
| `GET` | `/api/events` | Browse events (supports `?category=...&search=...`) | Public |
| `GET` | `/api/events/{id}` | Read full details of a specific event | Public |
| `POST` | `/api/events` | Create new event record (auto-creates EventTeam) | Authenticated |
| `PUT` | `/api/events/{id}` | Update event details | Owner / Editor / Admin |
| `DELETE` | `/api/events/{id}` | Permanently delete event | Owner / Admin |

### Shared Event Teams
| Method | Endpoint | Description | Access |
|---|---|---|:---:|
| `GET` | `/api/events/{id}/team` | Get organizing team and member roster | Authenticated |
| `POST` | `/api/events/{id}/team/members` | Invite new member by email (Editor/Coordinator/Viewer) | Owner / Admin |
| `PUT` | `/api/events/{id}/team/members/{user_id}` | Update member permission role | Owner / Admin |
| `DELETE` | `/api/events/{id}/team/members/{user_id}` | Remove member from organizing team | Owner / Admin |

### Administration Center
| Method | Endpoint | Description | Access |
|---|---|---|:---:|
| `GET` | `/api/admin/stats` | System overview KPIs (users, events, teams, sessions) | Admin Only |
| `GET` | `/api/admin/users` | Filtered user directory list | Admin Only |
| `PUT` | `/api/admin/users/{id}/status` | Ban or unban user with reason | Admin Only |
| `PUT` | `/api/admin/users/{id}/role` | Promote or demote user role (`User` ↔ `Admin`) | Admin Only |
| `GET` | `/api/admin/audit-logs` | Retrieve system-wide audit activity trail | Admin Only |
| `GET` | `/api/admin/export/csv` | Download CSV data export (`?type=events` or `?type=users`) | Admin Only |

---

## 🗄️ Database Schema & Entities

The application utilizes 5 core relational tables in SQLAlchemy ORM:

1. **`users`**: User records, hashed passwords, roles (`Admin` / `User`), ban status and reason.
2. **`user_sessions`**: Active refresh tokens tracked by SHA-256 hash, expiration date, and revocation flag (`is_revoked`).
3. **`events`**: Event titles, dates, descriptions, categories, capacity, status, and foreign key `creator_id`.
4. **`event_teams`**: 1-to-1 organizing team entity linked to each event.
5. **`team_members`**: Event collaborators with role tier (`Owner`, `Editor`, `Coordinator`, `Viewer`).
6. **`audit_logs`**: System audit records with action codes, timestamps, actors, and detailed event metadata.

---

## ☁️ Deployment Architecture (Vercel + Supabase)

The root repository includes `vercel.json` configuring dual-service serverless hosting:
- **Backend Service:** FastAPI ASGI application deployed as a Python serverless function handling `/api/*`.
- **Frontend Service:** React TypeScript application compiled with Vite, deployed to Vercel Edge CDN.
- **Database:** Supabase PostgreSQL cloud instance connected via `DATABASE_URL` with transaction pooling enabled.
