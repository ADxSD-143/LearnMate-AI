# API Docs

## Endpoints

### `GET /`
Returns a simple backend status message.

### `GET /health/`
Returns health status for uptime checks.

### `POST /api/v1/users/`
Accepts a user registration payload.

### `POST /api/v1/auth/login`
Accepts a user login payload.

### `GET /api/v1/users/me`
Returns the authenticated user's profile.

### `GET /api/v1/recommendations/`
Returns user-scoped rule-based recommendations, weak topics, and attendance.

### `GET /api/v1/study-plans/`
Returns a deterministic three-day baseline plan based on the user's weak topics.

### `POST /api/v1/predict/`
Accepts student features and returns a predicted score with recommendations.

### `POST /api/v1/materials/upload`
Uploads and processes a user-owned TXT, Markdown, or PDF document.

### `POST /api/v1/materials/{document_id}/ask`
Performs user-scoped keyword retrieval over processed document chunks. This is
not yet embedding-based semantic RAG.

All subject, topic, task, timetable, attendance, material, quiz,
recommendation, and study-plan endpoints require a bearer token unless
explicitly documented otherwise.
