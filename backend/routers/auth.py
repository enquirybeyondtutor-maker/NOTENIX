from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from database import get_db
from models import User
from security import hash_password, verify_password, create_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    full_name: str


def _user_dict(u: User) -> dict:
    return {
        "id": u.id, "email": u.email, "full_name": u.full_name,
        "plan": u.plan, "xp": u.xp, "streak": u.streak, "quiz_count": u.quiz_count,
    }


@router.post("/register")
async def register(data: RegisterIn, db: AsyncSession = Depends(get_db)):
    if len(data.password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters")
    existing = (await db.execute(select(User).where(User.email == data.email))).scalar_one_or_none()
    if existing:
        raise HTTPException(400, "An account with this email already exists")
    user = User(
        email=data.email.lower(),
        password_hash=hash_password(data.password),
        full_name=data.full_name.strip()[:120],
        last_active=datetime.utcnow(),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"access_token": create_token(user.id), "token_type": "bearer", "user": _user_dict(user)}


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = (await db.execute(select(User).where(User.email == form.username.lower()))).scalar_one_or_none()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(401, "Incorrect email or password")
    user.last_active = datetime.utcnow()
    await db.commit()
    return {"access_token": create_token(user.id), "token_type": "bearer", "user": _user_dict(user)}


@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    return _user_dict(user)
