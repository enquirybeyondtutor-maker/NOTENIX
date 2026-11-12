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


KS3_PRICES = {
    "GBP": 149, "AED": 699, "USD": 189, "EUR": 179, "AUD": 289,
    "NZD": 319, "SGD": 255, "CAD": 259, "INR": 16999, "THB": 5990,
}


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


def ks3_for_currency(currency: str | None) -> dict:
    """Notenix KS3 yearly price in this currency (KS3_PRICES env overrides the defaults)."""
    p = dict(KS3_PRICES)
    try:
        custom = json.loads(settings.ks3_prices or "{}")
        if isinstance(custom, dict) and custom:
            p = {k.upper(): float(v) for k, v in custom.items()}
    except Exception:
        pass
    cur = (currency or "GBP").upper()
    if cur not in p:
        cur = "GBP" if "GBP" in p else next(iter(p))
    return {"currency": cur, "amount": p[cur], "label": label(cur, p[cur])}


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
