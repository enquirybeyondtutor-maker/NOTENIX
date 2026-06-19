# Notenix — AI-Powered Active Learning Platform

Transform any notes into an intelligent study system using Claude AI (Opus 4.7).

## Architecture

```
notenix/
├── backend/               # FastAPI + 6 Claude agents
│   ├── agents/
│   │   ├── ingestion.py   # Agent 1: PDF/image/text extraction
│   │   ├── knowledge.py   # Agent 2: Topic & concept mapping (adaptive thinking)
│   │   ├── generator.py   # Agent 3: MCQ + flashcard + short-answer generation (streaming)
│   │   ├── tutor.py       # Agent 4: Multi-turn AI tutor (streaming + prompt cache)
│   │   ├── evaluator.py   # Agent 5: Answer grading (adaptive thinking)
│   │   └── scheduler.py   # Agent 6: Spaced revision plan (adaptive thinking)
│   ├── models/schemas.py
│   ├── main.py
│   └── requirements.txt
└── frontend/              # Next.js 14 App Router
    ├── app/
    │   ├── page.tsx                  # Upload landing
    │   ├── study/[id]/page.tsx       # MCQ / flashcard / short-answer practice
    │   ├── tutor/[id]/page.tsx       # AI tutor chat
    │   └── dashboard/[id]/page.tsx  # Analytics + revision plan
    ├── components/
    │   ├── upload/UploadZone.tsx
    │   ├── practice/QuestionCard.tsx
    │   ├── practice/FlashCard.tsx
    │   └── tutor/TutorChat.tsx
    └── lib/api.ts
```

## Setup

### 1. Backend

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

uvicorn main:app --reload --port 8000
```

### 2. Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

Open http://localhost:3000

## OpenAI Features Used

| Feature | Where |
|---|---|
| `gpt-4o` | All 6 agents |
| `response_format: json_object` | Agents 2, 5, 6 (guaranteed JSON output) |
| Streaming | Agents 3, 4 (generation, tutor) |
| Vision API | Agent 1 (image notes + scanned PDFs) |
| PyMuPDF | Agent 1 (fast PDF text extraction) |

## API Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/api/upload` | Upload notes → returns session_id + knowledge_map |
| GET | `/api/generate/{id}` | SSE stream: generate all question types |
| GET | `/api/questions/{id}` | Get questions (filter by type) |
| POST | `/api/evaluate/{id}` | Submit answer → score + feedback |
| POST | `/api/tutor/{id}` | SSE stream: AI tutor response |
| POST | `/api/schedule/{id}` | Generate spaced revision plan |
| GET | `/api/session/{id}` | Session details + performance |
| GET | `/api/health` | Health check |

## Production Notes

- Replace the in-memory `sessions` dict in `main.py` with Supabase
- Add authentication (Supabase Auth or Clerk)
- Deploy backend to Railway / Render, frontend to Vercel
- Set `ANTHROPIC_API_KEY` as an environment secret
