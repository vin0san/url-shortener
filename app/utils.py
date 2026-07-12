import secrets
from datetime import datetime, timedelta, timezone

def generate_short_key(length: int = 6) -> str:
    return secrets.token_urlsafe(length)[:length]

def calculate_expiration(days: int | None) -> datetime | None:
    if not days:
        return None
    
    return datetime.now(timezone.utc) + timedelta(days=days)