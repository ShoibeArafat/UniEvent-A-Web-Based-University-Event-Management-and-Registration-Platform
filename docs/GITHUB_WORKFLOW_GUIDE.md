# CSE309 GitHub Presentation & Workflow Guide (10 Marks)

> **Important:** As per your instructions, no remote push or merge has been performed to your GitHub repository. Follow this guide when you are ready to present your GitHub workflow to your instructor.

Your course instructor evaluates the GitHub presentation based on:
1. **GitHub Issue**
2. **Feature branch**
3. **Pull Request (PR)**
4. **Proper PR workflow**
5. **All relevant PRs merged into `main` before assessment**

---

## 📋 Step 1: Create the GitHub Issue

Go to your repository on GitHub and click **Issues** -> **New Issue**.

- **Title:**
  ```text
  Implement Event Management CRUD
  ```

- **Body (Markdown):**
  ```markdown
  ## Feature Description
  Implement the core Event Management feature for UniEvent as our Mid-Term MVP.

  ## Requirements
  - [x] Backend: FastAPI REST API with full CRUD endpoints (`POST`, `GET`, `GET by ID`, `PUT`, `DELETE`).
  - [x] Database: SQLAlchemy ORM model for `Event` with SQLite/Supabase support.
  - [x] Frontend: React 19 + TypeScript with responsive event cards, search, category filters, and modals.
  - [x] Integration: Frontend connects to FastAPI backend via Vite proxy and REST fetch services.
  ```

- Note down the issue number (e.g., `#1`).

---

## 🌿 Step 2: Create the Feature Branch

The instructor's naming convention is:
```text
{username}/#{issue_number}-{task_title}
```

Assuming your username is `shoibe` and the issue is `#1`:

```bash
# Ensure you are on main and up to date
git switch main
git pull

# Create the feature branch (quote the branch name because # is special in PowerShell/bash)
git switch -c "shoibe/#1-implement-event-management-crud"
```

---

## 💾 Step 3: Conventional Commits

The instructor requires **Conventional Commits**:
```text
<type>: <short summary> (#<issue_number>)
```

Example git commands to commit your work:

```bash
git add backend/
git commit -m "feat: implement event CRUD API and database model (#1)"

git add frontend/
git commit -m "feat: implement event management React frontend with CRUD modals (#1)"

git add docs/ README.md AGENTS.md
git commit -m "docs: add viva guide and workflow documentation (#1)"
```

Push your feature branch to your GitHub repository:
```bash
git push -u origin "shoibe/#1-implement-event-management-crud"
```

---

## 🔀 Step 4: Create the Pull Request (PR)

On GitHub, you will see a banner: **"Compare & pull request"**.

- **PR Title:**
  ```text
  feat: implement event management CRUD (#1)
  ```

- **PR Description (Markdown):**
  ```markdown
  ## Summary
  This PR implements the Event Management MVP feature for UniEvent (CSE309 Mid Project Assessment).

  ## Changes Included
  - **FastAPI Backend:**
    - `POST /api/events` - Create event with Pydantic validation.
    - `GET /api/events` - Read all events with search and category filter.
    - `GET /api/events/{id}` - Read single event details.
    - `PUT /api/events/{id}` - Update event record.
    - `DELETE /api/events/{id}` - Delete event record.
  - **Database:**
    - SQLAlchemy model `Event` with automated SQLite persistence and initial seed events.
  - **React 19 + TypeScript Frontend:**
    - Event cards grid with category and status pills.
    - Search bar and category filter tabs.
    - Create / Edit event modal with client validation.
    - Event detail modal (Read Single demonstration).
    - Delete confirmation modal and toast notification alerts.

  ## Issue Reference
  Closes #1
  ```

---

## 🏁 Step 5: Merge the Pull Request

- Review the PR on GitHub.
- Click **Merge pull request** -> **Confirm merge**.
- Notice that because of `Closes #1` in the description, Issue `#1` will automatically close on merge!
- Switch back to `main` locally:
  ```bash
  git switch main
  git pull
  ```

Now your GitHub repository has the exact Issue, Feature Branch, Conventional Commits, and Merged PR required to earn the full 10 marks for GitHub presentation!
