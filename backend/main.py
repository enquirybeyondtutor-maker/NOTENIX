import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from services.retention import purge_old_responses
from routers import auth, quiz, progress, leaderboard, payments, teacher, student_tests, admin, practice, marking


async def _retention_loop():
    """Purge expired student responses on boot, then once a day."""
    while True:
        try:
            n = await purge_old_responses()
            if n:
                print(f"[retention] purged responses from {n} record(s)")
        except Exception as e:  # never let the loop die
            print(f"[retention] purge failed: {e}")
        await asyncio.sleep(24 * 3600)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    task = asyncio.create_task(_retention_loop())
    try:
        yield
    finally:
        task.cancel()


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
app.include_router(practice.router)
app.include_router(marking.router)


@app.get("/health")
async def health():
    return {"status": "healthy", "version": "2.0"}


@app.get("/")
async def root():
    return {"name": "Notenix API", "docs": "/docs"}
