import os
import stripe
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

router = APIRouter(prefix="/api/payments", tags=["payments"])

# ─── Plans ───────────────────────────────────────────────────────────────────

PLANS = {
    "pro_monthly": {
        "name": "Pro Monthly",
        "price_usd": 499,          # cents → $4.99
        "interval": "month",
        "features": ["Unlimited uploads", "All question types", "BI Tutor chat", "Revision plans"],
    },
    "exam_pack": {
        "name": "Exam Pack",
        "price_usd": 999,          # cents → $9.99 one-time
        "interval": "one_time",
        "features": ["30-day access", "5 uploads", "All features", "No subscription"],
    },
}

# In-memory plan store — replace with DB in production
# key: user_email or session_id, value: plan info
user_plans: dict = {}


# ─── Schemas ─────────────────────────────────────────────────────────────────

class CheckoutRequest(BaseModel):
    plan: str               # "pro_monthly" | "exam_pack"
    user_email: str
    session_id: str = ""    # optional: notenix session to unlock after payment


# ─── Create Checkout Session ──────────────────────────────────────────────────

@router.post("/create-checkout")
async def create_checkout(body: CheckoutRequest):
    plan = PLANS.get(body.plan)
    if not plan:
        raise HTTPException(status_code=400, detail="Invalid plan")

    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="Stripe not configured. Set STRIPE_SECRET_KEY.")

    try:
        if plan["interval"] == "month":
            # Recurring subscription
            price = stripe.Price.create(
                unit_amount=plan["price_usd"],
                currency="usd",
                recurring={"interval": "month"},
                product_data={"name": plan["name"]},
            )
            checkout = stripe.checkout.Session.create(
                mode="subscription",
                line_items=[{"price": price.id, "quantity": 1}],
                customer_email=body.user_email,
                success_url=f"{FRONTEND_URL}/success?session_id={{CHECKOUT_SESSION_ID}}&plan={body.plan}",
                cancel_url=f"{FRONTEND_URL}/pricing",
                metadata={"notenix_session": body.session_id, "plan": body.plan},
            )
        else:
            # One-time payment
            price = stripe.Price.create(
                unit_amount=plan["price_usd"],
                currency="usd",
                product_data={"name": plan["name"]},
            )
            checkout = stripe.checkout.Session.create(
                mode="payment",
                line_items=[{"price": price.id, "quantity": 1}],
                customer_email=body.user_email,
                success_url=f"{FRONTEND_URL}/success?session_id={{CHECKOUT_SESSION_ID}}&plan={body.plan}",
                cancel_url=f"{FRONTEND_URL}/pricing",
                metadata={"notenix_session": body.session_id, "plan": body.plan},
            )

        return {"checkout_url": checkout.url, "checkout_id": checkout.id}

    except stripe.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─── Stripe Webhook ───────────────────────────────────────────────────────────

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature", "")

    try:
        if WEBHOOK_SECRET:
            event = stripe.Webhook.construct_event(payload, sig, WEBHOOK_SECRET)
        else:
            # Dev mode — no signature check
            import json
            event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if event["type"] in ("checkout.session.completed", "invoice.payment_succeeded"):
        obj = event["data"]["object"]
        email = obj.get("customer_email") or obj.get("customer_details", {}).get("email", "")
        meta = obj.get("metadata", {})
        plan = meta.get("plan", "pro_monthly")

        if email:
            user_plans[email] = {
                "plan": plan,
                "active": True,
                "stripe_session": obj.get("id"),
            }

    elif event["type"] in ("customer.subscription.deleted", "invoice.payment_failed"):
        obj = event["data"]["object"]
        email = obj.get("customer_email", "")
        if email and email in user_plans:
            user_plans[email]["active"] = False

    return JSONResponse({"status": "ok"})


# ─── Check Plan ───────────────────────────────────────────────────────────────

@router.get("/plan")
async def get_plan(email: str):
    info = user_plans.get(email)
    if info and info.get("active"):
        return {"plan": info["plan"], "active": True}
    return {"plan": "free", "active": True}


# ─── Plans Info (for pricing page) ───────────────────────────────────────────

@router.get("/plans")
async def list_plans():
    return PLANS
