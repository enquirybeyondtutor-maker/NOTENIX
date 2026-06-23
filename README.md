# Notenix v2

AI-powered GCSE & A-Level quiz platform built on a real past-paper knowledge base.

## Architecture

```
knowledge_base/        Real exam-paper PDFs (subject/board folders) — gitignored
ingestion/             One-time pipeline: PDF -> questions -> PostgreSQL + ChromaDB
backend/               FastAPI: auth, quiz (RAG), exam-mode AI marking, progress, payments
frontend/              Next.js (App Router), light purple theme, deploys to Vercel
```

## Quiz modes
- **Quiz mode (free)** — AI-generated MCQs from your real questions, auto-graded.
- **Exam mode (pro)** — real past-paper questions, AI marks written answers vs. a generated mark scheme.

## Stack
- FastAPI + asyncpg (PostgreSQL via Neon)
- ChromaDB for semantic retrieval
- Anthropic Claude for generation + marking
- Next.js 15 on Vercel (proxies `/api/*` -> Render, so no CORS)

## Local dev
```bash
# Backend
cd backend && pip install -r requirements.txt && uvicorn main:app --reload
# Frontend
cd frontend && npm install && npm run dev
# Ingestion (one-time)
cd ingestion && python run_ingestion.py
```
