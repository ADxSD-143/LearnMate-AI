# Architecture

## Backend
FastAPI exposes authenticated REST endpoints for users, academic structure,
tasks, timetable, attendance, study materials, quizzes, recommendations, and
study plans. Business logic is kept in service modules and ownership is
checked against the authenticated user before private resources are returned.

## ML Layer
Preprocessing, model training, model loading, and inference are separated under
`backend/app/ml`. The current prediction endpoint is an explicitly labelled
deterministic baseline; it is not presented as a trained production model.

## Documents and RAG
Uploaded text, Markdown, and PDF files are stored under a generated
user-scoped filename during development. Text is extracted and chunked into
user-owned database records. Retrieval is currently keyword-based and does not
yet provide embeddings, pgvector search, or an external LLM generation layer.
Answers and study artifacts must therefore be treated as grounded scaffolding,
not production-grade semantic RAG or generative AI.

## Frontend
The Vite/React frontend currently provides a buildable application shell with
backend health and API documentation links. Feature screens and authenticated
TanStack Query workflows remain future integration work.

## Database
Development can use `AUTO_CREATE_TABLES=true`. Production should set it to
`false` and apply schema changes through a migration workflow before startup.

## Data
Raw and processed datasets are isolated under `datasets/`, while trained artifacts live under `trained_models/`.
