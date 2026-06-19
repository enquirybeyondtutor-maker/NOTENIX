from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from database import get_db
from models.user import User
from routers.auth import get_current_user
from config import get_settings
import stripe
from datetime import datetime

router = APIRouter(prefix="/payments", tags=["payments"])
settings = get_settings()
stripe.api_key = settings.stripe_secret_key

PLANS = {
    "monthly": {"price_id": settings.stripe_monthly_price_id, "amount": 10000, "currency": "gbp"},
    "yearly": {"price_id": settings.stripe_yearly_price_id, "amount": 110000, "currency": "gbp"},
}


class CreateCheckoutRequest(BaseModel):
    plan: str  # monthly | yearly


@router.post("/create-checkout")
async def create_checkout(req: CreateCheckoutRequest, current_user: User = Depends(get_current_user)):
    if req.plan not in PLANS:
        raise HTTPException(status_code=400, detail="Invalid plan")
    plan = PLANS[req.plan]

    if not current_user.stripe_customer_id:
        customer = stripe.Customer.create(email=current_user.email, name=current_user.full_name)
        customer_id = customer.id
    else:
        customer_id = current_user.stripe_customer_id

    session = stripe.checkout.Session.create(
        customer=customer_id,
        payment_method_types=["card"],
        line_items=[{"price": plan["price_id"], "quantity": 1}],
        mode="subscription",
        success_url=f"{settings.frontend_url}/dashboard?subscribed=true",
        cancel_url=f"{settings.frontend_url}/pricing",
        metadata={"user_id": current_user.id, "plan": req.plan},
    )
    return {"checkout_url": session.url}


@router.post("/webhook")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.stripe_webhook_secret)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session.get("metadata", {}).get("user_id")
        plan = session.get("metadata", {}).get("plan", "monthly")
        customer_id = session.get("customer")
        subscription_id = session.get("subscription")

        if user_id:
            result = await db.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            if user:
                user.stripe_customer_id = customer_id
                user.stripe_subscription_id = subscription_id
                user.subscription_tier = plan
                user.subscription_status = "active"
                await db.commit()

    elif event["type"] in ("customer.subscription.deleted", "customer.subscription.unpaid"):
        sub = event["data"]["object"]
        customer_id = sub.get("customer")
        result = await db.execute(select(User).where(User.stripe_customer_id == customer_id))
        user = result.scalar_one_or_none()
        if user:
            user.subscription_status = "inactive"
            user.subscription_tier = "free"
            await db.commit()

    return {"status": "ok"}


@router.get("/plans")
async def get_plans():
    return {
        "monthly": {"price": 100, "currency": "GBP", "interval": "month", "features": ["Unlimited quizzes", "All subjects", "AI analysis", "Progress tracking", "SRS system"]},
        "yearly": {"price": 1100, "currency": "GBP", "interval": "year", "savings": "Save £100 vs monthly", "features": ["Everything in monthly", "Mock exam mode", "Study planner", "Parent dashboard", "Priority support"]},
    }
