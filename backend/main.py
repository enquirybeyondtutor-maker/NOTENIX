import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from services.retention import purge_old_responses
from services.sittings import auto_submit_expired
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


async def _sittings_loop():
    """Finalize timed sittings whose clock has run out, every minute."""
    while True:
        try:
            n = await auto_submit_expired()
            if n:
                print(f"[sittings] auto-submitted {n} expired sitting(s)")
        except Exception as e:
            print(f"[sittings] sweep failed: {e}")
        await asyncio.sleep(60)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    tasks = [asyncio.create_task(_retention_loop()), asyncio.create_task(_sittings_loop())]
    try:
        yield
    finally:
        for t in tasks:
            t.cancel()


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


@app.get("/ping")
async def ping():
    """Keep-warm target: also runs a trivial query so the ping wakes the database
    (Neon), not just the web service. Point an uptime pinger here every ~10 min."""
    from sqlalchemy import text
    from database import engine
    db_ok = False
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        pass
    return {"ok": True, "db": db_ok}


@app.get("/")
async def root():
    return {"name": "Notenix API", "docs": "/docs"}
