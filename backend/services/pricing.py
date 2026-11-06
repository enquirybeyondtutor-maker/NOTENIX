"""Beyond Tutors student subscription price in each student's billing currency.

Prices live in SUBSCRIPTION_PRICES (Render env, JSON) so they can change without a deploy.
The student's currency is set by the admin when the account is issued.
"""
import json
from config import settings

DEFAULT_PRICES = {
    "GBP": 49, "AED": 229, "USD": 65, "EUR": 59, "AUD": 99,
    "NZD": 109, "SGD": 85, "CAD": 89, "INR": 5499,
}
SYMBOLS = {"GBP": "£", "USD": "$", "EUR": "€", "AUD": "A$", "NZD": "NZ$", "SGD": "S$", "CAD": "C$", "INR": "₹"}
NAMES = {"GBP": "UK", "AED": "UAE", "USD": "US", "EUR": "Europe", "AUD": "Australia",
         "NZD": "New Zealand", "SGD": "Singapore", "CAD": "Canada", "INR": "India"}


KS3_PRICES = {
    "GBP": 149, "AED": 699, "USD": 189, "EUR": 179, "AUD": 289,
    "NZD": 319, "SGD": 255, "CAD": 259, "INR": 16999,
}


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
