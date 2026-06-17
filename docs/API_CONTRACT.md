# API Contract

## Base URL

http://127.0.0.1:8000/api/

## Core Endpoints

| Endpoint                    | Method | Description                            |
| --------------------------- | ------ | -------------------------------------- |
| /api/                       | GET    | API status information                 |
| /api/health/                | GET    | Service health check                   |
| /api/subjects/              | GET    | Retrieve subjects, topics, and lessons |
| /api/lessons/               | GET    | Retrieve available lessons             |
| /api/lessons/{id}/          | GET    | Retrieve lesson details                |
| /api/lessons/{id}/complete/ | POST   | Complete lesson and award rewards      |
| /api/profile/               | GET    | Retrieve learner profile information   |

## Completion Logic

Successful completion grants:

* XP rewards
* Coin rewards
* Progress updates

Repeated completion attempts do not generate additional rewards.

