# EduRPG Platform

Backend: Django REST Framework + JWT. Frontend: React + Vite.

## Backend setup

Run from `backend/`:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Core API:

- `POST /api/register/`
- `POST /api/token/`
- `POST /api/token/refresh/`
- `GET /api/me/`
- `GET /api/courses/`
- `GET /api/courses/<id>/lessons/`
- `POST /api/lessons/<id>/complete/`
- `GET /api/achievements/`
- `GET /api/leaderboard/`
- `GET /api/stats/`

## Checks

Run from `backend/`:

```powershell
python manage.py makemigrations --check --dry-run
python manage.py test
python manage.py check
```

## Production blockers

Before deploying, replace the development settings:

- move `SECRET_KEY` to environment variables;
- set `DEBUG = False`;
- restrict `ALLOWED_HOSTS`;
- replace `CORS_ALLOW_ALL_ORIGINS = True` with explicit origins;
- switch from SQLite to a production database.
