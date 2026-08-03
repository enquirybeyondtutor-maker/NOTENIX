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
        elif dialect == "sqlite":
            # SQLite lacks ADD COLUMN IF NOT EXISTS — check PRAGMA first.
            cols = {c[1] for c in (await conn.execute(text("PRAGMA table_info(users)"))).all()}
            if "role" not in cols:
                await conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'student'"))
            if "is_active" not in cols:
                await conn.execute(text("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1"))
            tcols = (await conn.execute(text("PRAGMA table_info(tests)"))).all()
            if tcols and "share_token" not in {c[1] for c in tcols}:
                await conn.execute(text("ALTER TABLE tests ADD COLUMN share_token VARCHAR(64)"))
