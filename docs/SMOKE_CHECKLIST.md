# Smoke Checklist

Use this checklist before a demo, commit, or practice report recording.

## Backend Run Check

- Open a terminal.
- Run:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

- Confirm backend starts at:

```text
http://127.0.0.1:8000/
```

## Frontend Run Check

- Open a second terminal.
- Run:

```powershell
cd frontend
npm run dev
```

- Confirm frontend starts, usually at:

```text
http://127.0.0.1:5173/
```

## API Checks

Open these URLs in a browser or API client:

- `http://127.0.0.1:8000/api/health/`
- `http://127.0.0.1:8000/api/subjects/`
- `http://127.0.0.1:8000/api/lessons/1/`
- `http://127.0.0.1:8000/api/profile/`

Expected:

- Health returns status `ok`.
- Subjects includes Biology / Genetics / lesson data if seeded.
- Lesson detail returns `What is DNA?` if lesson 1 exists.
- Profile returns username, level, XP, and coins.

## Page Checks

- `/` shows Home dashboard.
- `/map` shows Learning Map.
- `/lessons/1` shows lesson detail.
- `/profile` shows RPG player profile.
- `/duels` shows planned Duels module.
- `/shop` shows planned Shop module.

## Lesson Complete Check

- Open `/lessons/1`.
- Click `Завершить урок`.
- Confirm a polished completion/reward message appears.
- Click again or refresh and complete again.
- Confirm repeated farming is prevented or shown as already completed.

## Build Check

Run:

```powershell
cd frontend
npm run build
```

Expected:

- Build completes without errors.

## Git Status Check Before Commit

Run:

```powershell
git status --short
```

Before committing, confirm no generated/local files are included:

- `backend/db.sqlite3`
- `__pycache__/`
- `.venv/`
- `node_modules/`
- frontend build output
