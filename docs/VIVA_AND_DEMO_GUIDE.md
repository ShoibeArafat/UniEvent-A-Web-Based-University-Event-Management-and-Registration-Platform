# CSE309 Mid Project Assessment — Viva & Feature Demonstration Guide

This guide prepares you for all **5 Viva Questions** required by your course instructor for the **UniEvent — Event Management MVP (30 Marks)**.

---

## 🎯 Question 1: Demonstrate all CRUD operations in your frontend

During your demonstration, perform the operations in this order:

### 1. Read List (Display all records)
- Open http://localhost:5173.
- Show the **Events Grid** displaying the seeded events (Tech Fest 2026, Programming Contest, Robotics Workshop, etc.).
- Demonstrate the **live search bar**: Type "Robotics" — show how the list dynamically filters to only relevant events.
- Demonstrate the **category filter pills**: Click "Competition" — show that only competition events appear; click "All" to reset.

### 2. Create (Add a new record)
- Click the **"+ New Event"** button on the navbar or hero section.
- Fill out the form:
  - **Title:** `Cloud Computing & DevOps Workshop`
  - **Category:** `Workshop`
  - **Date:** `2026-11-29`
  - **Location:** `Lab 402, Engineering Building`
  - **Organizer:** `Cloud & AI Club`
  - **Max Capacity:** `75`
  - **Status:** `Upcoming`
  - **Description:** `Hands-on workshop on containerization with Docker and cloud deployment on Vercel.`
- Click **"Create Event"**.
- Point out:
  - The form closes smoothly.
  - A green toast alert appears: `Event "Cloud Computing & DevOps Workshop" published successfully!`.
  - The new event card immediately appears in the grid.
  - The total events count in the navbar updates.

### 3. Read Single (View one specific record)
- Click the **"Details"** button on your newly created event (or any card).
- The **Event Detail Modal** pops up:
  - Point out that it fetches the fresh record from `GET /api/events/{id}`.
  - Show the full formatted date, venue, organizer badge, maximum capacity, status, and full multi-line description.
  - Point out the API callout badge at the bottom: `GET /api/events/{id} (Status 200 OK)`.

### 4. Update (Edit an existing record)
- Click **"Edit"** from either the event card or inside the detail modal.
- The pre-populated modal opens with the current values.
- Change:
  - **Location:** `Grand Ballroom & Cloud Lab`
  - **Max Capacity:** `100`
- Click **"Save Changes"**.
- Point out:
  - The toast alert confirms: `Event "Cloud Computing & DevOps Workshop" updated successfully!`.
  - The card immediately reflects the new location and capacity.

### 5. Delete (Remove a record)
- Click the red **"Delete"** button on the event card.
- The **Confirm Delete** dialog opens:
  - Explain that we prevent accidental deletion by asking for user confirmation.
- Click **"Confirm Delete"**.
- Point out:
  - The toast confirms the deletion message from the server.
  - The card disappears from the grid.
  - The total counter decreases by 1.

---

## 🌐 Question 2: Explain how requests travel from React frontend to FastAPI backend using browser Developer Tools

Open **Developer Tools** in Chrome / Edge / Firefox by pressing `F12` or `Ctrl + Shift + I`, then navigate to the **Network** tab. Ensure the filter is set to **Fetch/XHR**.

### How to explain the request flow to the instructor:

1. **User Action:**
   - *"When I click 'Create Event' in React, the `handleSubmit` function in `EventModal.tsx` intercepts the form event, prevents default page reload (`e.preventDefault()`), and calls `createEvent(formData)` from `services/api.ts`."*

2. **HTTP Request dispatch:**
   - *"The browser initiates an asynchronous `fetch()` request with method `POST` to URL `/api/events`."*
   - In DevTools Network tab, click on the `/api/events` request row:
     - **Request URL:** `http://localhost:5173/api/events` (or your Vercel URL).
     - **Request Method:** `POST`
     - **Request Headers:**
       - `Content-Type: application/json`
     - **Request Payload (Body):**
       ```json
       {
         "title": "Cloud Computing & DevOps Workshop",
         "description": "Hands-on workshop...",
         "location": "Lab 402",
         "event_date": "2026-11-29",
         "organizer": "Cloud & AI Club",
         "category": "Workshop",
         "capacity": 75,
         "status": "Upcoming"
       }
       ```

3. **Vite Proxy / Vercel Routing:**
   - *"During local development, `vite.config.ts` has a proxy configuration that forwards all `/api/*` traffic to our FastAPI backend running on port 8000 (`http://localhost:8000`). On Vercel, `vercel.json` routes `/api/(.*)` directly to the FastAPI serverless backend."*

4. **FastAPI Processing & Pydantic Validation:**
   - *"FastAPI receives the request at route `@router.post('/api/events')`. It automatically deserializes and validates the JSON payload against the Pydantic schema `EventCreate`. If any field is missing or invalid, FastAPI automatically returns an HTTP `422 Unprocessable Entity`."*

5. **SQLAlchemy ORM & Database Persistence:**
   - *"FastAPI injects an active database session `db: Session` via `Depends(get_db)`. An `Event` SQLAlchemy model instance is created, added via `db.add()`, and committed via `db.commit()`. The SQLite database writes the record to disk."*

6. **HTTP Response:**
   - *"FastAPI serializes the saved record into `EventResponse` and returns HTTP status code `201 Created` with the JSON object containing the assigned auto-increment `id`, `created_at`, and `updated_at`."*
   - Show the instructor the **Response** tab in DevTools:
     ```json
     {
       "id": 6,
       "title": "Cloud Computing & DevOps Workshop",
       "status": "Upcoming",
       ...
     }
     ```

7. **React State Update:**
   - *"React awaits the parsed JSON promise, updates its state via `setEvents(...)`, and re-renders the UI to show the newly added event without reloading the page."*

---

## 📡 Question 3: Explain your REST API endpoints

Explain the 5 core REST endpoints implemented in `backend/routes/events.py`:

| Method | Endpoint | Status Code | Description |
|---|---|:---:|---|
| `POST` | `/api/events` | `201 Created` | Creates a new event. Body contains `EventCreate` schema. Returns the saved event with assigned `id`. |
| `GET` | `/api/events` | `200 OK` | Retrieves an array of all events. Supports optional query parameters `?category=...` and `?search=...`. Ordered chronologically by `event_date`. |
| `GET` | `/api/events/{id}` | `200 OK` (or `404`) | Fetches a single event record by ID. If not found, raises `HTTPException(404, detail="Event with ID {id} not found")`. |
| `PUT` | `/api/events/{id}` | `200 OK` (or `404`) | Updates an event by ID. Body contains `EventUpdate` with optional fields. Returns the updated record. |
| `DELETE` | `/api/events/{id}` | `200 OK` (or `404`) | Deletes an event by ID. Returns a confirmation JSON message: `{"message": "...", "id": id}`. |

Point out that interactive documentation is automatically generated by FastAPI at:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 📮 Question 4: Demonstrate API requests using Postman / Swagger

You can demonstrate using Postman or FastAPI's built-in **Swagger UI** (`/docs`).

### Sample Requests:

#### 1. GET all events
- **Method:** `GET`
- **URL:** `http://localhost:8000/api/events`
- **Query Params (Optional):**
  - `category`: `Technology`
  - `search`: `Fest`
- **Expected Status:** `200 OK`

#### 2. POST create event
- **Method:** `POST`
- **URL:** `http://localhost:8000/api/events`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
  ```json
  {
    "title": "Cybersecurity Capture The Flag 2026",
    "description": "University-wide ethical hacking and reverse engineering competition.",
    "location": "Cyber Lab 101",
    "event_date": "2026-12-01",
    "organizer": "Information Security Club",
    "category": "Competition",
    "capacity": 80,
    "status": "Upcoming"
  }
  ```
- **Expected Status:** `201 Created`

#### 3. GET single event
- **Method:** `GET`
- **URL:** `http://localhost:8000/api/events/1`
- **Expected Status:** `200 OK`

#### 4. PUT update event
- **Method:** `PUT`
- **URL:** `http://localhost:8000/api/events/1`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
  ```json
  {
    "capacity": 400,
    "location": "University Grand Auditorium"
  }
  ```
- **Expected Status:** `200 OK`

#### 5. DELETE event
- **Method:** `DELETE`
- **URL:** `http://localhost:8000/api/events/1`
- **Expected Status:** `200 OK`
- **Response:**
  ```json
  {
    "message": "Event 'Tech Fest 2026' (ID 1) was deleted successfully.",
    "id": 1
  }
  ```

---

## 🗃️ Question 5: Explain database models, relationships, and backend integration

Explain the database architecture implemented in `backend/database.py` and `backend/models.py`:

1. **ORM Choice:**
   - *"We use **SQLAlchemy ORM (v2.0)** with a declarative base (`declarative_base()`). This decouples our business logic from raw SQL and protects against SQL injection attacks through automatic parameter binding."*

2. **The `Event` Model:**
   - Table name: `events`
   - Attributes:
     - `id`: Integer, primary key, autoincrementing.
     - `title`: String(200), indexed for fast lookup.
     - `description`: Text, holds full event details.
     - `location`: String(200), physical venue.
     - `event_date`: String(50), ISO date string (`YYYY-MM-DD`).
     - `organizer`: String(150), department or student club.
     - `category`: String(100), indexed for category filtering queries.
     - `capacity`: Integer, default 100.
     - `status`: String(50), default "Upcoming".
     - `created_at` / `updated_at`: DateTime timestamps.

3. **Session Management:**
   - *"We use a generator dependency `get_db()` with Python's `yield` statement. Each incoming HTTP request receives its own isolated database session `SessionLocal()`, and when the request finishes, the `finally:` block guarantees the session is closed, preventing database connection leaks."*

4. **Multi-Environment Adaptability:**
   - *"In development, it uses SQLite (`sqlite:///./events.db`). For cloud deployments or Supabase, setting the `DATABASE_URL` environment variable automatically redirects SQLAlchemy to connect to PostgreSQL / Supabase with zero code changes."*
