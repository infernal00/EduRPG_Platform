# EduRPG_Platform

EduRPG_Platform is an MVP learning platform that presents lessons as RPG-style quests. The current demo flow shows a learner dashboard, a learning map, a lesson detail page, reward completion, and a profile screen.

## Tech Stack

- Backend: Django, Django REST Framework, SQLite for local MVP data
- Frontend: React, Vite, React Router, CSS
- Demo target: local development on `127.0.0.1`

## Backend Setup

From the repository root:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install django djangorestframework django-cors-headers
python manage.py migrate
python manage.py runserver
```

Backend base URL:

```text
http://127.0.0.1:8000/
```

Useful API checks:

```text
http://127.0.0.1:8000/api/subjects/
http://127.0.0.1:8000/api/lessons/1/
http://127.0.0.1:8000/api/profile/
```

## Frontend Setup

From the repository root:

```powershell
cd frontend
npm install
npm run dev
```

Frontend dev URL is usually:

```text
http://127.0.0.1:5173/
```

Production build check:

```powershell
cd frontend
npm run build
```

## Demo Flow

1. Open the Home dashboard.
2. Click `Learning Map`.
3. Open the Biology / Genetics lesson node: `What is DNA?`.
4. Click `Complete lesson`.
5. Open `Profile` and show level, XP, coins, achievements, and stats.
6. Briefly show `Duels` and `Shop` as planned modules.

## Current Features

- Dark RPG-style dashboard UI.
- Subject/topic/lesson learning map.
- Lesson detail page with reward panel.
- Lesson completion endpoint with XP and coin rewards.
- Completion is protected from repeated farming by backend progress records.
- Profile endpoint for demo user stats.
- Duels and Shop placeholder screens for planned modules.
- Silent polished frontend fallback data for demo continuity.

## Planned Features

- Authentication and multiple user profiles.
- Real quiz questions inside lessons.
- PvP duels and ranked learning battles.
- Shop inventory, purchases, boosts, and cosmetics.
- Expanded subject content and progress tracking.
- Leaderboards and richer achievement logic.

## Team Workflow

Recommended branch flow:

```text
feature branches -> develop -> main
```

- Create feature branches for focused work.
- Merge completed features into `develop`.
- Use `main` for stable demo/release-ready code.

## Repository Hygiene

Do not commit local/generated files such as:

- `backend/db.sqlite3`
- `__pycache__/`
- `.venv/`
- `node_modules/`
- build output such as `dist/`
