# Architecture

## Backend
FastAPI exposes REST endpoints for health checks, auth, and predictions.

## ML Layer
Preprocessing, model training, model loading, and inference are separated under `backend/app/ml`.

## Frontend
The frontend is reserved for the learner-facing application and dashboard flows.

## Data
Raw and processed datasets are isolated under `datasets/`, while trained artifacts live under `trained_models/`.
