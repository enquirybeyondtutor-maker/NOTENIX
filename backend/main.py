from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import auth, quiz, progress, leaderboard, payments, teacher, student_tests, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Notenix API", version="2.0", lifespan=lifespan)

# Frontend proxies /api/* through Vercel (same-origin), so CORS is permissive and credential-free.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(quiz.router)
app.include_router(progress.router)
app.include_router(leaderboard.router)
app.include_router(payments.router)
app.include_router(teacher.router)
app.include_router(student_tests.router)
app.include_router(admin.router)


@app.get("/health")
async def health():
    return {"status": "healthy", "version": "2.0"}


@app.get("/")
async def root():
    return {"name": "Notenix API", "docs": "/docs"}
