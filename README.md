# 🍳 Recipes Full-Stack Application

Monorepo with FastAPI backend and React + TypeScript frontend.

## Quick Start (one command)
```bash
docker compose -f docker-compose.yml up --build
```

- Backend Swagger: http://localhost:8000/docs
- Frontend SPA:    http://localhost:3000

## Backend
- FastAPI, in-memory SQLite
- Endpoints:
  - `GET /recipes?search=text`
  - `GET /recipes/{id}`
- Global exception handling, validation, logging, SOLID-ish layering
- Tests: `cd backend && pytest`

## Frontend
- React + TS (Vite)
- Global search, client-side sort/filter, responsive grid, lazy-loaded grid
- Tests: `cd frontend && npm test`

## Dev Notes
- In-memory DB is seeded from https://dummyjson.com/recipes at startup.
- For production persistence, replace `DATABASE_URL` in `backend/app/config.py`.
