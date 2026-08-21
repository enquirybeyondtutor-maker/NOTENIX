from urllib.parse import urlsplit, urlunsplit
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from config import settings


def _prepare(url: str):
    """Convert to async driver and strip libpq-only query params asyncpg rejects
    (sslmode, channel_binding, etc.). Returns (url, connect_args)."""
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)

    connect_args = {}
    if "asyncpg" in url:
        parts = urlsplit(url)
        had_ssl = "sslmode=require" in (parts.query or "") or "sslmode=verify" in (parts.query or "")
        # drop the entire query string — Neon params (sslmode, channel_binding) are libpq-only
        url = urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
        if had_ssl or "neon.tech" in parts.netloc:
            connect_args = {"ssl": True}
    return url, connect_args


DATABASE_URL, connect_args = _prepare(settings.database_url)

engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with SessionLocal() as session:
        yield session


async def init_db():
    import models  # noqa: F401  (register models)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await run_migrations()


async def run_migrations():
    """Idempotent, additive-only migrations for columns create_all cannot add to
    pre-existing tables. Safe to run on every boot."""
    from sqlalchemy import text

    dialect = engine.dialect.name  # 'postgresql' | 'sqlite'
    async with engine.begin() as conn:
        if dialect == "postgresql":
            await conn.execute(text(
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT 'student'"
            ))
            await conn.execute(text(
                "UPDATE users SET role = 'student' WHERE role IS NULL"
            ))
            await conn.execute(text(
                "ALTER TABLE tests ADD COLUMN IF NOT EXISTS share_token VARCHAR(64)"
            ))
            await conn.execute(text(
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE"
            ))
            await conn.execute(text(
                "UPDATE users SET is_active = TRUE WHERE is_active IS NULL"
            ))
            # Email-verification columns. is_verified DEFAULT TRUE keeps existing
            # accounts verified; only new signups are set False by register().
            await conn.execute(text(
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_verified BOOLEAN DEFAULT TRUE"
            ))
            await conn.execute(text(
                "UPDATE users SET is_verified = TRUE WHERE is_verified IS NULL"
            ))
            await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS otp_hash VARCHAR(255)"))
            await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS otp_expires_at TIMESTAMP"))
            await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS otp_attempts INTEGER DEFAULT 0"))
            # Written-answer practice (extended-response). All additive.
            await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS can_write BOOLEAN DEFAULT FALSE"))
            await conn.execute(text("UPDATE users SET can_write = FALSE WHERE can_write IS NULL"))
            await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS name_changed_at TIMESTAMP"))
            await conn.execute(text("ALTER TABLE tests ADD COLUMN IF NOT EXISTS mode VARCHAR(20) DEFAULT 'mcq'"))
            await conn.execute(text("UPDATE tests SET mode = 'mcq' WHERE mode IS NULL"))
            await conn.execute(text("ALTER TABLE tests ADD COLUMN IF NOT EXISTS is_library BOOLEAN DEFAULT FALSE"))
            await conn.execute(text("UPDATE tests SET is_library = FALSE WHERE is_library IS NULL"))
            await conn.execute(text("ALTER TABLE tests ADD COLUMN IF NOT EXISTS kind VARCHAR(20) DEFAULT 'test'"))
            await conn.execute(text("UPDATE tests SET kind = 'test' WHERE kind IS NULL"))
            await conn.execute(text("ALTER TABLE test_attempts ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'graded'"))
            await conn.execute(text("UPDATE test_attempts SET status = 'graded' WHERE status IS NULL"))
            await conn.execute(text("ALTER TABLE test_attempts ADD COLUMN IF NOT EXISTS marked_by INTEGER"))
            await conn.execute(text("ALTER TABLE test_attempts ADD COLUMN IF NOT EXISTS answer_images JSON"))
            await conn.execute(text("ALTER TABLE test_attempts ADD COLUMN IF NOT EXISTS question_times JSON"))
            await conn.execute(text("ALTER TABLE test_attempts ADD COLUMN IF NOT EXISTS purged_at TIMESTAMP"))
            # Server-anchored timer + draft autosave
            await conn.execute(text("ALTER TABLE test_assignments ADD COLUMN IF NOT EXISTS started_at TIMESTAMP"))
            await conn.execute(text("ALTER TABLE test_assignments ADD COLUMN IF NOT EXISTS draft_answers JSON"))
            # Integrity signals
            await conn.execute(text("ALTER TABLE test_attempts ADD COLUMN IF NOT EXISTS focus_lost_count INTEGER DEFAULT 0"))
            await conn.execute(text("ALTER TABLE test_attempts ADD COLUMN IF NOT EXISTS time_away_seconds INTEGER DEFAULT 0"))
            await conn.execute(text("ALTER TABLE test_attempts ADD COLUMN IF NOT EXISTS paste_attempts INTEGER DEFAULT 0"))
            await conn.execute(text("ALTER TABLE test_attempts ADD COLUMN IF NOT EXISTS auto_submitted BOOLEAN DEFAULT FALSE"))
            await conn.execute(text("ALTER TABLE test_attempts ADD COLUMN IF NOT EXISTS ai_flag VARCHAR(20)"))
            await conn.execute(text("ALTER TABLE test_attempts ADD COLUMN IF NOT EXISTS ai_notes TEXT"))
            await conn.execute(text("ALTER TABLE test_attempts ADD COLUMN IF NOT EXISTS copy_attempts INTEGER DEFAULT 0"))
            await conn.execute(text("ALTER TABLE test_attempts ADD COLUMN IF NOT EXISTS fullscreen_exits INTEGER DEFAULT 0"))
            await conn.execute(text("ALTER TABLE test_attempts ADD COLUMN IF NOT EXISTS burst_flags INTEGER DEFAULT 0"))
        elif dialect == "sqlite":
            # SQLite lacks ADD COLUMN IF NOT EXISTS — check PRAGMA first.
            cols = {c[1] for c in (await conn.execute(text("PRAGMA table_info(users)"))).all()}
            if "role" not in cols:
                await conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'student'"))
            if "is_active" not in cols:
                await conn.execute(text("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1"))
            if "is_verified" not in cols:
                await conn.execute(text("ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT 1"))
            if "otp_hash" not in cols:
                await conn.execute(text("ALTER TABLE users ADD COLUMN otp_hash VARCHAR(255)"))
            if "otp_expires_at" not in cols:
                await conn.execute(text("ALTER TABLE users ADD COLUMN otp_expires_at TIMESTAMP"))
            if "otp_attempts" not in cols:
                await conn.execute(text("ALTER TABLE users ADD COLUMN otp_attempts INTEGER DEFAULT 0"))
            if "can_write" not in cols:
                await conn.execute(text("ALTER TABLE users ADD COLUMN can_write BOOLEAN DEFAULT 0"))
            if "name_changed_at" not in cols:
                await conn.execute(text("ALTER TABLE users ADD COLUMN name_changed_at TIMESTAMP"))
            tcols = {c[1] for c in (await conn.execute(text("PRAGMA table_info(tests)"))).all()}
            if tcols and "share_token" not in tcols:
                await conn.execute(text("ALTER TABLE tests ADD COLUMN share_token VARCHAR(64)"))
            if tcols and "mode" not in tcols:
                await conn.execute(text("ALTER TABLE tests ADD COLUMN mode VARCHAR(20) DEFAULT 'mcq'"))
            if tcols and "is_library" not in tcols:
                await conn.execute(text("ALTER TABLE tests ADD COLUMN is_library BOOLEAN DEFAULT 0"))
            if tcols and "kind" not in tcols:
                await conn.execute(text("ALTER TABLE tests ADD COLUMN kind VARCHAR(20) DEFAULT 'test'"))
            acols = {c[1] for c in (await conn.execute(text("PRAGMA table_info(test_attempts)"))).all()}
            if acols and "status" not in acols:
                await conn.execute(text("ALTER TABLE test_attempts ADD COLUMN status VARCHAR(20) DEFAULT 'graded'"))
            if acols and "marked_by" not in acols:
                await conn.execute(text("ALTER TABLE test_attempts ADD COLUMN marked_by INTEGER"))
            if acols and "answer_images" not in acols:
                await conn.execute(text("ALTER TABLE test_attempts ADD COLUMN answer_images JSON"))
            if acols and "question_times" not in acols:
                await conn.execute(text("ALTER TABLE test_attempts ADD COLUMN question_times JSON"))
            if acols and "purged_at" not in acols:
                await conn.execute(text("ALTER TABLE test_attempts ADD COLUMN purged_at TIMESTAMP"))
            for col, ddl in [
                ("focus_lost_count", "INTEGER DEFAULT 0"), ("time_away_seconds", "INTEGER DEFAULT 0"),
                ("paste_attempts", "INTEGER DEFAULT 0"), ("auto_submitted", "BOOLEAN DEFAULT 0"),
                ("ai_flag", "VARCHAR(20)"), ("ai_notes", "TEXT"),
                ("copy_attempts", "INTEGER DEFAULT 0"), ("fullscreen_exits", "INTEGER DEFAULT 0"),
                ("burst_flags", "INTEGER DEFAULT 0"),
            ]:
                if acols and col not in acols:
                    await conn.execute(text(f"ALTER TABLE test_attempts ADD COLUMN {col} {ddl}"))
            ascols = {c[1] for c in (await conn.execute(text("PRAGMA table_info(test_assignments)"))).all()}
            if ascols and "started_at" not in ascols:
                await conn.execute(text("ALTER TABLE test_assignments ADD COLUMN started_at TIMESTAMP"))
            if ascols and "draft_answers" not in ascols:
                await conn.execute(text("ALTER TABLE test_assignments ADD COLUMN draft_answers JSON"))
