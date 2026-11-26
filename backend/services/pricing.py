"""Beyond Tutors student subscription price in each student's billing currency.

Prices live in SUBSCRIPTION_PRICES (Render env, JSON) so they can change without a deploy.
The student's currency is set by the admin when the account is issued.
"""
import json
from config import settings

DEFAULT_PRICES = {
    "GBP": 49, "AED": 229, "USD": 65, "EUR": 59, "AUD": 99,
    "NZD": 109, "SGD": 85, "CAD": 89, "INR": 5499, "THB": 2100,
}
SYMBOLS = {"GBP": "£", "USD": "$", "EUR": "€", "AUD": "A$", "NZD": "NZ$", "SGD": "S$", "CAD": "C$", "INR": "₹", "THB": "฿"}
NAMES = {"GBP": "UK", "AED": "UAE", "USD": "US", "EUR": "Europe", "AUD": "Australia",
         "NZD": "New Zealand", "SGD": "Singapore", "CAD": "Canada", "INR": "India",
         "THB": "Thailand"}


# Notenix KS3 by year group: [first, second, third year] = UK Years 7/8/9, or Grades 5/6/7 on the
# US (Middle School) and Ontario tracks. Agreed Nov 2026: list GBP 169/189/209, offer GBP 159/179/199.
# Other currencies scaled from the old flat price (GBP 149) by the same ratio and rounded.
# While the offer is on (settings.ks3_offer, until settings.ks3_offer_until), families pay KS3_PRICES
# and see KS3_LIST_PRICES struck through; after that they pay KS3_LIST_PRICES.
KS3_LIST_PRICES = {
    "GBP": (169, 189, 209), "AED": (799, 889, 979), "USD": (219, 239, 269), "EUR": (199, 229, 249),
    "AUD": (329, 369, 409), "NZD": (359, 409, 449), "SGD": (289, 325, 359), "CAD": (295, 329, 365),
    "INR": (19499, 21499, 23999), "THB": (6790, 7590, 8390),
}
KS3_PRICES = {   # offer prices
    "GBP": (159, 179, 199), "AED": (749, 839, 929), "USD": (199, 229, 249), "EUR": (189, 215, 239),
    "AUD": (309, 349, 389), "NZD": (339, 379, 429), "SGD": (269, 305, 339), "CAD": (275, 309, 345),
    "INR": (17999, 19999, 22499), "THB": (6390, 7190, 7990),
}
KS3_FIRST_YEAR = {"us": 5, "on": 5}   # first grade of each grade-based track; UK KS3 starts at Year 7


# Notenix SAT, one year. Lower than KS3: SAT families are mostly in India, the Gulf and Asia.
SAT_PRICES = {
    "USD": 129, "INR": 7999, "AED": 469, "GBP": 99, "SGD": 169, "AUD": 199,
    "EUR": 119, "NZD": 219, "CAD": 179, "THB": 3990,
}


# Notenix GCSE, one subject for one year (students outside Beyond Tutors). Agreed Nov 2026: GBP 99.
GCSE_PRICES = {
    "GBP": 99, "USD": 129, "INR": 7999, "AED": 469, "SGD": 169, "AUD": 199,
    "EUR": 119, "NZD": 219, "CAD": 179, "THB": 3990,
}


# All four GCSE subjects together for one year. Agreed Nov 2026: GBP 349 (four singles would be GBP 396).
GCSE_BUNDLE_PRICES = {
    "GBP": 349, "USD": 449, "INR": 27999, "AED": 1649, "SGD": 599, "AUD": 699,
    "EUR": 419, "NZD": 769, "CAD": 629, "THB": 13990,
}


def gcse_bundle_for_currency(currency: str | None) -> dict:
    """Price of the four-subject GCSE bundle (GCSE_BUNDLE_PRICES env overrides the defaults)."""
    p = dict(GCSE_BUNDLE_PRICES)
    try:
        custom = json.loads(getattr(settings, "gcse_bundle_prices", "") or "{}")
        if isinstance(custom, dict) and custom:
            p = {k.upper(): float(v) for k, v in custom.items()}
    except Exception:
        pass
    cur = (currency or "GBP").upper()
    if cur not in p:
        cur = "GBP" if "GBP" in p else next(iter(p))
    return {"currency": cur, "amount": p[cur], "label": label(cur, p[cur])}


def gcse_for_currency(currency: str | None) -> dict:
    """Notenix GCSE yearly price per subject in this currency (GCSE_PRICES env overrides the defaults)."""
    p = dict(GCSE_PRICES)
    try:
        custom = json.loads(getattr(settings, "gcse_prices", "") or "{}")
        if isinstance(custom, dict) and custom:
            p = {k.upper(): float(v) for k, v in custom.items()}
    except Exception:
        pass
    cur = (currency or "GBP").upper()
    if cur not in p:
        cur = "GBP" if "GBP" in p else next(iter(p))
    return {"currency": cur, "amount": p[cur], "label": label(cur, p[cur])}


def sat_for_currency(currency: str | None) -> dict:
    """Notenix SAT yearly price in this currency (SAT_PRICES env overrides the defaults)."""
    p = dict(SAT_PRICES)
    try:
        custom = json.loads(getattr(settings, "sat_prices", "") or "{}")
        if isinstance(custom, dict) and custom:
            p = {k.upper(): float(v) for k, v in custom.items()}
    except Exception:
        pass
    cur = (currency or "USD").upper()
    if cur not in p:
        cur = "USD" if "USD" in p else next(iter(p))
    return {"currency": cur, "amount": p[cur], "label": label(cur, p[cur])}


def ks3_tier(year: int | None, track: str | None = None) -> int:
    """0, 1 or 2: which price step a KS3 year (7-9) or track grade (5-7) is on."""
    first = KS3_FIRST_YEAR.get(track or "", 7)
    try:
        return min(2, max(0, int(year) - first))
    except (TypeError, ValueError):
        return 0


def ks3_offer_until():
    """When the KS3 offer ends (aware UTC datetime), or None for no end date."""
    from datetime import datetime
    raw = (getattr(settings, "ks3_offer_until", "") or "").strip()
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def ks3_offer_on() -> bool:
    """The offer is switched on and its end time hasn't passed."""
    from datetime import datetime, timezone
    if not settings.ks3_offer:
        return False
    until = ks3_offer_until()
    if until and until.tzinfo is None:
        until = until.replace(tzinfo=timezone.utc)
    return until is None or datetime.now(timezone.utc) < until


def _ks3_table(offer: bool) -> dict[str, tuple]:
    if not offer:
        return dict(KS3_LIST_PRICES)
    p = dict(KS3_PRICES)
    try:
        custom = json.loads(settings.ks3_prices or "{}")
        if isinstance(custom, dict) and custom:
            p = {k.upper(): tuple(float(x) for x in v) if isinstance(v, (list, tuple)) else (float(v),) * 3
                 for k, v in custom.items()}
    except Exception:
        pass
    return p


def ks3_for_currency(currency: str | None, tier: int = 0) -> dict:
    """Notenix KS3 yearly price for one year group (tier 0/1/2) in this currency.
    While the offer is on, "was"/"was_label" carry the list price to show struck through."""
    offer = ks3_offer_on()
    p = _ks3_table(offer)
    cur = (currency or "GBP").upper()
    if cur not in p:
        cur = "GBP" if "GBP" in p else next(iter(p))
    tier = min(max(int(tier or 0), 0), len(p[cur]) - 1)
    amount = float(p[cur][tier])
    out = {"currency": cur, "amount": amount, "label": label(cur, amount)}
    was = KS3_LIST_PRICES.get(cur)
    if offer and was and was[tier] > amount:
        out.update(was=float(was[tier]), was_label=label(cur, was[tier]))
    return out


def ks3_for_user(u, currency: str | None = None) -> dict:
    """The KS3 price for this student's own year group (Year 6 children on Year 7 work pay Year 7)."""
    tier = ks3_tier(getattr(u, "ks3_year", None), getattr(u, "ks3_track", None))
    return ks3_for_currency(currency or getattr(u, "billing_currency", None), tier)


def ks3_table() -> dict[str, list[dict]]:
    """Every currency's three year-group prices, for the public checkout page."""
    return {c: [ks3_for_currency(c, t) for t in range(3)] for c in _ks3_table(ks3_offer_on())}


# Normal Notenix price: one course for a year, for students outside Beyond Tutors (courses that
# have no price table of their own, i.e. not GCSE, the GCSE bundle or SAT). GBP follows
# config.revision_price. The admin can change or add currencies on the Admin page; that table is
# kept in the app_settings table (key "normal_prices") and cached here.
NORMAL_PRICES = {
    "GBP": float(settings.revision_price), "AED": 699, "USD": 189, "EUR": 179, "AUD": 289,
    "NZD": 319, "SGD": 255, "CAD": 259, "INR": 16999, "THB": 5990,
}
_db_normal: dict[str, float] = {}


def normal_prices() -> dict[str, float]:
    return dict(_db_normal) if _db_normal else dict(NORMAL_PRICES)


def normal_for_currency(currency: str | None) -> dict:
    p = normal_prices()
    cur = (currency or "GBP").upper()
    if cur not in p:
        cur = "GBP" if "GBP" in p else next(iter(p))
    return {"currency": cur, "amount": p[cur], "label": label(cur, p[cur])}


async def load_db_prices(db) -> None:
    """Refresh the cached admin-set normal prices from the database."""
    from sqlalchemy import select
    from models import AppSetting
    row = (await db.execute(select(AppSetting).where(AppSetting.key == "normal_prices"))).scalar_one_or_none()
    _db_normal.clear()
    if row:
        try:
            data = json.loads(row.value or "{}")
            if isinstance(data, dict):
                _db_normal.update({k.upper(): float(v) for k, v in data.items()})
        except Exception:
            pass


async def save_normal_prices(db, table: dict[str, float]) -> None:
    from sqlalchemy import select
    from models import AppSetting
    value = json.dumps({k.upper(): float(v) for k, v in table.items()})
    row = (await db.execute(select(AppSetting).where(AppSetting.key == "normal_prices"))).scalar_one_or_none()
    if row:
        row.value = value
    else:
        db.add(AppSetting(key="normal_prices", value=value))
    await db.commit()
    await load_db_prices(db)


def prices() -> dict[str, float]:
    try:
        custom = json.loads(settings.subscription_prices or "{}")
        if isinstance(custom, dict) and custom:
            return {k.upper(): float(v) for k, v in custom.items()}
    except Exception:
        pass
    return dict(DEFAULT_PRICES)


def label(currency: str, amount: float) -> str:
    n = f"{amount:,.0f}" if float(amount).is_integer() else f"{amount:,.2f}"
    sym = SYMBOLS.get(currency)
    return f"{sym}{n}" if sym else f"{currency} {n}"


def for_currency(currency: str | None) -> dict:
    p = prices()
    cur = (currency or "GBP").upper()
    if cur not in p:
        cur = "GBP" if "GBP" in p else next(iter(p))
    return {"currency": cur, "amount": p[cur], "label": label(cur, p[cur])}


def options() -> list[dict]:
    return [{**for_currency(c), "region": NAMES.get(c, c)} for c in prices()]
