"""Dates sent by the browser arrive with a timezone ("2026-11-11T00:00:00.000Z" from
toISOString()), but every DateTime column stores naive UTC. Postgres (asyncpg) refuses
timezone-aware values for those columns, so convert to UTC and drop the timezone on the
way in. Use `UtcDateTime` for any datetime field in a request body."""
from datetime import datetime, timezone
from typing import Annotated

from pydantic import AfterValidator


def to_utc_naive(v: datetime | None) -> datetime | None:
    if v is not None and v.tzinfo is not None:
        return v.astimezone(timezone.utc).replace(tzinfo=None)
    return v


UtcDateTime = Annotated[datetime, AfterValidator(to_utc_naive)]
