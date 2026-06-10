# Инструкция по установке EduRPG Backend

## Шаг 1 — Замени файлы

Скопируй все файлы из этой папки в соответствующие места проекта:

```
config/settings.py  → backend/config/settings.py
config/urls.py      → backend/config/urls.py
core/models.py      → backend/core/models.py
core/views.py       → backend/core/views.py
core/urls.py        → backend/core/urls.py
core/serializers.py → backend/core/serializers.py
core/achievements.py→ backend/core/achievements.py
core/admin.py       → backend/core/admin.py
core/apps.py        → backend/core/apps.py
```

## Шаг 2 — Добавь в конец config/settings.py

```python
AUTH_USER_MODEL = 'core.User'
```

## Шаг 3 — Установи зависимости

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install djangorestframework-simplejwt
```

## Шаг 4 — Миграции и запуск

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API работает на:
- http://127.0.0.1:8000/api/          ← список всех эндпоинтов
- http://127.0.0.1:8000/admin/        ← админка
