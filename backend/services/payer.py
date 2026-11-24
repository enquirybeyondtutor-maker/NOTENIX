"""Payer details shared by every "I've paid" form."""
from datetime import date

from fastapi import HTTPException


def clean_dob(value: str | None) -> str | None:
    """The payer's date of birth (YYYY-MM-DD), optional. Wise sometimes asks for it to confirm
    who sent a transfer, so having it lets the admin match the payment faster."""
    v = (value or "").strip()
    if not v:
        return None
    try:
        d = date.fromisoformat(v)
    except ValueError:
        raise HTTPException(400, "Please enter the date of birth as a full date, or leave it blank.")
    if not date(1900, 1, 1) <= d <= date.today():
        raise HTTPException(400, "Please check the date of birth of the person who paid.")
    return d.isoformat()
