from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models import User
from security import get_current_user
from config import settings

router = APIRouter(prefix="/payments", tags=["payments"])


@router.get("/plans")
async def plans():
    return {
        "free": {"price": 0, "features": [
            f"{settings.free_quiz_limit} free quizzes",
            "Smart MCQ quizzes", "Progress tracking", "Leaderboard access",
        ]},
        "pro": {"price": 9.99, "features": [
            "Unlimited quizzes", "Exam mode (real past papers)",
            "Instant marking of written answers", "All subjects & boards", "Priority support",
        ]},
    }


@router.post("/create-checkout")
async def create_checkout(user: User = Depends(get_current_user)):
    if not settings.stripe_secret_key:
        raise HTTPException(503, "Payments not configured yet.")
    import stripe
    stripe.api_key = settings.stripe_secret_key
    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": settings.stripe_price_id, "quantity": 1}],
        customer_email=user.email,
        success_url=f"{settings.frontend_url}/dashboard?upgraded=true",
        cancel_url=f"{settings.frontend_url}/pricing",
        metadata={"user_id": str(user.id)},
    )
    return {"url": session.url}


@router.post("/webhook")
async def webhook(request: Request, db: AsyncSession = Depends(get_db)):
    if not settings.stripe_webhook_secret:
        raise HTTPException(503, "Webhook not configured")
    import stripe
    payload = await request.body()
    sig = request.headers.get("stripe-signature", "")
    try:
        event = stripe.Webhook.construct_event(payload, sig, settings.stripe_webhook_secret)
    except Exception:
        raise HTTPException(400, "Invalid webhook signature")
    if event["type"] == "checkout.session.completed":
        uid = int(event["data"]["object"]["metadata"]["user_id"])
        user = (await db.execute(select(User).where(User.id == uid))).scalar_one_or_none()
        if user:
            user.plan = "pro"
            await db.commit()
    return {"received": True}
