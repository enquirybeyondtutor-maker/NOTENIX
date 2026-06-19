from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from database import init_db
from services.rag_service import seed_knowledge_base
from routers import auth, quiz, progress, payments, knowledge, leaderboard, social
from config import get_settings

settings = get_settings()
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await seed_knowledge_base()
    yield


app = FastAPI(
    title="Notenix API",
    description="AI-powered GCSE & A-Level quiz platform",
    version="1.1.0",
    lifespan=lifespan,
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Session (required for Google OAuth)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

# CORS
_origins = list({
    settings.frontend_url,
    "http://localhost:3000",
    "https://notenix.com",
    "https://www.notenix.com",
})
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(quiz.router)
app.include_router(progress.router)
app.include_router(payments.router)
app.include_router(knowledge.router)
app.include_router(leaderboard.router)
app.include_router(social.router)


@app.get("/")
async def root():
    return {"message": "Notenix API v1.1", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
