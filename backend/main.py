import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from services.retention import purge_old_responses
from services.sittings import auto_submit_expired
from routers import auth, quiz, progress, leaderboard, payments, teacher, student_tests, admin, practice, marking, reports, requests, notes, papers, sync, ks3, help, doubt, courses, sat, exam, series
from routers.payments import expire_pro_plans


async def _retention_loop():
    """Purge expired student responses and lapsed bank-transfer Pro plans on boot, then once a day."""
    while True:
        try:
            n = await purge_old_responses()
            if n:
                print(f"[retention] purged responses from {n} record(s)")
        except Exception as e:  # never let the loop die
            print(f"[retention] purge failed: {e}")
        try:
            n = await expire_pro_plans()
            if n:
                print(f"[plans] {n} Pro plan(s) expired")
        except Exception as e:
            print(f"[plans] expiry sweep failed: {e}")
        await asyncio.sleep(24 * 3600)


async def _ks3_loop():
    """KS3 free-trial parent emails and weekly progress emails, checked every 6 hours.
    (Hourly checks woke the database 24x a day; the welcome email is sent at sign-up.)"""
    from services.ks3 import run_sequence
    while True:
        try:
            n = await run_sequence()
            if n:
                print(f"[ks3] sent {n} trial email(s)")
        except Exception as e:
            print(f"[ks3] sequence failed: {e}")
        try:
            from services.sat_progress import run_weekly as sat_weekly
            n = await sat_weekly()
            if n:
                print(f"[sat] sent {n} weekly progress email(s)")
        except Exception as e:
            print(f"[sat] weekly emails failed: {e}")
        try:
            from services.exam_progress import run_weekly as exam_weekly
            n = await exam_weekly()
            if n:
                print(f"[exam] sent {n} weekly progress email(s)")
        except Exception as e:
            print(f"[exam] weekly emails failed: {e}")
        try:
            from services.doubt import run_sequence as doubt_sequence
            n = await doubt_sequence()
            if n:
                print(f"[doubt] sent {n} plan email(s)")
        except Exception as e:
            print(f"[doubt] sequence failed: {e}")
        try:
            from services.ks3 import run_yearly
            st = await run_yearly()
            if any(st.values()):
                print(f"[ks3] yearly: {st}")
        except Exception as e:
            print(f"[ks3] yearly run failed: {e}")
        await asyncio.sleep(6 * 3600)


async def _sittings_loop():
    """Finalize timed sittings whose clock has run out. Sleeps until the next deadline
    (at most an hour) rather than polling, so the database can scale to zero when idle."""
    from services.sittings import wait_for_next
    while True:
        next_deadline = None
        try:
            n, next_deadline = await auto_submit_expired()
            if n:
                print(f"[sittings] auto-submitted {n} expired sitting(s)")
        except Exception as e:
            print(f"[sittings] sweep failed: {e}")
            await asyncio.sleep(60)
            continue
        await wait_for_next(next_deadline)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    try:   # admin-set normal Notenix prices (Admin page) into the pricing cache
        from database import SessionLocal
        from services import pricing
        async with SessionLocal() as db:
            await pricing.load_db_prices(db)
    except Exception as e:
        print(f"[pricing] couldn't load admin prices: {e}")
    tasks = [asyncio.create_task(_retention_loop()), asyncio.create_task(_sittings_loop()), asyncio.create_task(_ks3_loop())]
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
app.include_router(reports.router)
app.include_router(requests.router)
app.include_router(notes.router)
app.include_router(papers.router)
app.include_router(sync.router)
app.include_router(ks3.router)
app.include_router(help.router)
app.include_router(doubt.router)
app.include_router(courses.router)
app.include_router(sat.router)
app.include_router(exam.router)
app.include_router(series.router)


@app.get("/health")
async def health():
    return {"status": "healthy", "version": "2.0"}


@app.get("/ping")
async def ping():
    """Checks the database too. Do NOT point a keep-warm pinger here: that keeps Neon
    awake 24/7 and uses up its compute allowance. Use /health for keep-warm."""
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
