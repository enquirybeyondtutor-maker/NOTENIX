from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr, field_validator
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer
from database import get_db
from models.user import User
from config import get_settings
from slowapi import Limiter
from slowapi.util import get_remote_address
import uuid
import re
import httpx

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
limiter = Limiter(key_func=get_remote_address)
serializer = URLSafeTimedSerializer(settings.secret_key)


# ── Models ──────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @field_validator("full_name")
    @classmethod
    def name_clean(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Full name too short")
        return re.sub(r"[<>\"'%;()&+]", "", v)[:100]


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def pw_check(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


# ── Helpers ──────────────────────────────────────────────────────────────────

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def _user_dict(user: User) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "is_verified": user.is_verified,
        "subscription_tier": user.subscription_tier,
        "subscription_status": user.subscription_status,
        "xp_points": user.xp_points or 0,
        "streak_days": user.streak_days or 0,
        "free_quizzes_used": user.free_quizzes_used or 0,
        "free_quiz_limit": user.free_quiz_limit or 3,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        if not user_id:
            raise exc
    except JWTError:
        raise exc
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise exc
    return user


async def _send_verification_email(email: str, token: str):
    """Send verification email — falls back to console log if SMTP not configured."""
    verify_url = f"{settings.frontend_url}/verify-email?token={token}"
    if not settings.mail_username:
        print(f"[DEV] Verification link for {email}: {verify_url}")
        return
    try:
        from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
        conf = ConnectionConfig(
            MAIL_USERNAME=settings.mail_username,
            MAIL_PASSWORD=settings.mail_password,
            MAIL_FROM=settings.mail_from,
            MAIL_PORT=settings.mail_port,
            MAIL_SERVER=settings.mail_server,
            MAIL_FROM_NAME=settings.mail_from_name,
            MAIL_STARTTLS=settings.mail_starttls,
            MAIL_SSL_TLS=settings.mail_ssl_tls,
            USE_CREDENTIALS=True,
        )
        msg = MessageSchema(
            subject="Verify your Notenix account",
            recipients=[email],
            body=f"""
            <h2>Welcome to Notenix!</h2>
            <p>Click the link below to verify your email address:</p>
            <a href="{verify_url}" style="background:#a855f7;color:white;padding:12px 24px;border-radius:8px;text-decoration:none;display:inline-block;">
                Verify Email
            </a>
            <p>Link expires in 24 hours. If you didn't register, ignore this email.</p>
            """,
            subtype="html",
        )
        fm = FastMail(conf)
        await fm.send_message(msg)
    except Exception as e:
        print(f"[WARN] Email send failed: {e}")
        print(f"[DEV] Verification link: {verify_url}")


async def _send_reset_email(email: str, token: str):
    reset_url = f"{settings.frontend_url}/reset-password?token={token}"
    if not settings.mail_username:
        print(f"[DEV] Password reset link for {email}: {reset_url}")
        return
    try:
        from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
        conf = ConnectionConfig(
            MAIL_USERNAME=settings.mail_username,
            MAIL_PASSWORD=settings.mail_password,
            MAIL_FROM=settings.mail_from,
            MAIL_PORT=settings.mail_port,
            MAIL_SERVER=settings.mail_server,
            MAIL_FROM_NAME=settings.mail_from_name,
            MAIL_STARTTLS=settings.mail_starttls,
            MAIL_SSL_TLS=settings.mail_ssl_tls,
            USE_CREDENTIALS=True,
        )
        msg = MessageSchema(
            subject="Reset your Notenix password",
            recipients=[email],
            body=f"""
            <h2>Password Reset Request</h2>
            <p>Click below to reset your password. This link expires in 1 hour.</p>
            <a href="{reset_url}" style="background:#06b6d4;color:white;padding:12px 24px;border-radius:8px;text-decoration:none;display:inline-block;">
                Reset Password
            </a>
            <p>If you didn't request this, ignore this email.</p>
            """,
            subtype="html",
        )
        fm = FastMail(conf)
        await fm.send_message(msg)
    except Exception as e:
        print(f"[WARN] Email send failed: {e}")
        print(f"[DEV] Reset link: {reset_url}")


# ── Routes ───────────────────────────────────────────────────────────────────

@router.post("/register", response_model=TokenResponse)
@limiter.limit("10/minute")
async def register(request: Request, req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(User.email == req.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        id=str(uuid.uuid4()),
        email=req.email,
        hashed_password=pwd_context.hash(req.password),
        full_name=req.full_name,
        is_verified=False,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    verify_token = serializer.dumps(user.email, salt="email-verify")
    await _send_verification_email(user.email, verify_token)

    token = create_access_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer", "user": _user_dict(user)}


@router.post("/login", response_model=TokenResponse)
@limiter.limit("20/minute")
async def login(request: Request, form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == form.username))
    user = result.scalar_one_or_none()
    if not user or not pwd_context.verify(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = create_access_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer", "user": _user_dict(user)}


@router.get("/verify-email")
async def verify_email(token: str, db: AsyncSession = Depends(get_db)):
    try:
        email = serializer.loads(token, salt="email-verify", max_age=86400)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired verification link")
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_verified = True
    await db.commit()
    return RedirectResponse(url=f"{settings.frontend_url}/dashboard?verified=true")


@router.post("/resend-verification")
async def resend_verification(current_user: User = Depends(get_current_user)):
    if current_user.is_verified:
        raise HTTPException(status_code=400, detail="Already verified")
    verify_token = serializer.dumps(current_user.email, salt="email-verify")
    await _send_verification_email(current_user.email, verify_token)
    return {"message": "Verification email sent"}


@router.post("/forgot-password")
@limiter.limit("5/minute")
async def forgot_password(request: Request, req: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == req.email))
    user = result.scalar_one_or_none()
    # Always return success to avoid email enumeration
    if user:
        token = serializer.dumps(user.email, salt="pw-reset")
        await _send_reset_email(user.email, token)
    return {"message": "If that email exists, a reset link has been sent"}


@router.post("/reset-password")
async def reset_password(req: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    try:
        email = serializer.loads(req.token, salt="pw-reset", max_age=3600)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired reset link")
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = pwd_context.hash(req.new_password)
    await db.commit()
    return {"message": "Password updated successfully"}


@router.get("/google/login")
async def google_login(request: Request):
    if not settings.google_client_id:
        raise HTTPException(status_code=501, detail="Google OAuth not configured")
    from authlib.integrations.starlette_client import OAuth
    oauth = OAuth()
    oauth.register(
        name="google",
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )
    redirect_uri = f"{settings.app_url}/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, db: AsyncSession = Depends(get_db)):
    if not settings.google_client_id:
        raise HTTPException(status_code=501, detail="Google OAuth not configured")
    from authlib.integrations.starlette_client import OAuth
    oauth = OAuth()
    oauth.register(
        name="google",
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )
    token_data = await oauth.google.authorize_access_token(request)
    userinfo = token_data.get("userinfo", {})
    email = userinfo.get("email")
    full_name = userinfo.get("name", "Google User")

    if not email:
        raise HTTPException(status_code=400, detail="Could not get email from Google")

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        user = User(
            id=str(uuid.uuid4()),
            email=email,
            hashed_password=pwd_context.hash(str(uuid.uuid4())),
            full_name=full_name,
            is_verified=True,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    jwt_token = create_access_token({"sub": user.id})
    return RedirectResponse(url=f"{settings.frontend_url}/dashboard?token={jwt_token}")


@router.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return _user_dict(current_user)
