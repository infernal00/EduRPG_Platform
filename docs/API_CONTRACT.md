# API Contract

Base URL for local development:

```text
http://127.0.0.1:8000/api/
```

## Endpoint Table

| Endpoint | Method | Purpose | Notes |
|---|---:|---|---|
| `/api/` | GET | API home/status metadata | Useful quick backend sanity check. |
| `/api/health/` | GET | Health check | Returns service status and version. |
| `/api/subjects/` | GET | List active subjects with topics and lessons | Main data source for Home and Map. |
| `/api/lessons/` | GET | List active lessons | Supports optional `subject_id` and `topic_id` query params. |
| `/api/lessons/<id>/` | GET | Lesson detail | Main data source for Lesson page. |
| `/api/lessons/<id>/complete/` | POST | Complete lesson and award XP/coins | Uses demo user; prevents repeated farming. |
| `/api/profile/` | GET | Demo user profile | Main data source for Home/Profile stats. |

## Example Response Shapes

### GET `/api/subjects/`

```json
[
  {
    "id": 1,
    "name": "Biology",
    "description": "",
    "icon": "biology",
    "is_active": true,
    "created_at": "2026-06-01T12:00:00Z",
    "topics": [
      {
        "id": 1,
        "title": "Genetics",
        "description": "",
        "order": 0,
        "lessons": [
          {
            "id": 1,
            "title": "What is DNA?",
            "content": "",
            "level": "beginner",
            "xp_reward": 30,
            "coins_reward": 15,
            "order": 0,
            "is_active": true,
            "topic_id": 1,
            "topic_title": "Genetics",
            "subject_id": 1,
            "subject_name": "Biology"
          }
        ]
      }
    ]
  }
]
```

### GET `/api/lessons/1/`

```json
{
  "id": 1,
  "title": "What is DNA?",
  "content": "Lesson content here.",
  "level": "beginner",
  "xp_reward": 30,
  "coins_reward": 15,
  "order": 0,
  "is_active": true,
  "topic_id": 1,
  "topic_title": "Genetics",
  "subject_id": 1,
  "subject_name": "Biology"
}
```

### POST `/api/lessons/1/complete/`

Completed response:

```json
{
  "status": "completed",
  "message": "Lesson completed successfully.",
  "lesson_id": 1,
  "lesson_title": "What is DNA?",
  "xp_gained": 30,
  "coins_gained": 15,
  "profile": {
    "username": "demo",
    "level": 1,
    "xp": 30,
    "coins": 15
  }
}
```

Already completed response:

```json
{
  "status": "already_completed",
  "message": "Lesson was already completed.",
  "lesson_id": 1,
  "lesson_title": "What is DNA?",
  "xp_gained": 0,
  "coins_gained": 0,
  "profile": {
    "username": "demo",
    "level": 1,
    "xp": 30,
    "coins": 15
  }
}
```

### GET `/api/profile/`

```json
{
  "username": "demo",
  "level": 1,
  "xp": 30,
  "coins": 15,
  "updated_at": "2026-06-01T12:00:00Z"
}
```

## Frontend Developer Notes

- Frontend should keep polished fallback data for demo continuity if an API request fails.
- Do not show raw backend failure text during presentation mode.
- Treat `completed` and `already_completed` as successful lesson states in the UI.
- Use `subject.icon` keys such as `biology`, `math`, `physics`, `programming`, and `english` for local subject icons.
- Lesson completion currently uses the shared demo user created by the backend.
