# AGENTS.md

Instructions for AI coding agents (and developers) working in this repository.

## Project

**UniEvent**: University Event Management and Registration Platform.
- Architecture: FastAPI backend (`backend/`) + Vite/React/TypeScript frontend (`frontend/`), deployed together on Vercel (`vercel.json` routes `/api/*` to backend, static frontend handles UI).
- Requirements and design:
  - MVP Feature: **Event Management (CRUD)**.
  - Future Releases (Beta/Final): Student registration, QR ticket generation, attendance, certificates, RBAC.
- Do not build out-of-scope Beta items while Mid-Term MVP work is in progress.

---

## GitHub Presentation & Branch Naming Conventions (10 Marks)

Every feature or bug fix starts from a GitHub Issue. Branch names follow:

```
{username}/#{issue_number}-{task_title}
```

### Rules:
- `{username}`: your name / GitHub handle (e.g. `shoibe`).
- `{issue_number}`: the GitHub issue number, prefixed with `#`.
- `{task_title}`: the issue title in lowercase kebab-case (letters, digits and `-` only, no spaces or punctuation, max ~50 characters).
- Always branch from an up-to-date `main`.

### Example:
| Issue | Branch |
|---|---|
| #1 Implement Event Management CRUD | `shoibe/#1-implement-event-management-crud` |

```bash
git switch main
git pull
git switch -c "shoibe/#1-implement-event-management-crud"
```

---

## Commits

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <short summary> (#<issue_number>)
```

| Type | Use for |
|---|---|
| `feat` | A new feature or endpoint (e.g. event CRUD, frontend cards) |
| `fix` | A bug fix |
| `docs` | Documentation only (`docs/`, README, AGENTS.md) |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `style` | Formatting only, no code meaning change |
| `chore` | Dependencies, config, tooling (`requirements.txt`, `package.json`, `vercel.json`) |

### Rules:
- Summary in lowercase imperative mood ("add", not "added" or "adds"), no full stop, max ~72 characters.
- End with the issue reference, e.g. `(#1)`.
- Never commit secrets, `.env` files, `node_modules/`, `.venv/` or `frontend/dist/`.

### Examples:
```
feat: implement event CRUD REST API endpoints in FastAPI (#1)
feat: add event management dashboard UI in React TypeScript (#1)
docs: add viva guide and postman documentation (#1)
```

---

## Pull Requests

- One pull request per issue, from the feature branch into `main`.
- PR title uses the same format as commits, e.g. `feat: implement event management CRUD (#1)`.
- PR description must include `Closes #{issue_number}` so the issue closes on merge.
- Merge the PR into `main` before assessment.

---

## Running Locally

### Backend (Terminal 1)
```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1       # On Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
fastapi dev main.py             # Runs on http://localhost:8000
```
- Interactive API Docs (Swagger): http://localhost:8000/docs
- Alternative Docs (ReDoc): http://localhost:8000/redoc

### Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev                     # Runs on http://localhost:5173
```
- Open http://localhost:5173 to interact with the full dashboard.
- Requests to `/api/*` are automatically proxied to `http://localhost:8000`.
