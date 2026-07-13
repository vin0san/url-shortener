from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import Url
from app.utils import generate_short_key, calculate_expiration
from app.schemas import RequestShorten, ResponseShorten
from app.config import settings

router = APIRouter()

RESERVED_KEYS = {"admin", "api", "health", "shorten", "docs", "openapi.json"}
MAX_KEY_GEN_ATTEMPTS = 5


def _resolve_short_key(payload: RequestShorten, db: Session) -> str:
    if payload.custom_key:
        if payload.custom_key.lower() in RESERVED_KEYS:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "This key is reserved.")
        existing = db.query(Url).filter(Url.short_key == payload.custom_key).first()
        if existing:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "This custom key is already taken.")
        return payload.custom_key

    return generate_short_key()

@router.post("/shorten", response_model=ResponseShorten)
def shorten_url(payload: RequestShorten, db: Session = Depends(get_db)):
    is_custom = bool(payload.custom_key)
    key = _resolve_short_key(payload, db)

    attempts = 1 if is_custom else MAX_KEY_GEN_ATTEMPTS
    for attempt in range(attempts):
        db_url = Url(
            long_url=str(payload.long_url),
            short_key=key,
            expires_at=calculate_expiration(payload.expiration_days),
        )
        try:
            db.add(db_url)
            db.commit()
            db.refresh(db_url)
            break
        except IntegrityError:
            db.rollback()
            if is_custom:
                raise HTTPException(status.HTTP_409_CONFLICT, "Key taken by a concurrent request.")
            key = generate_short_key()
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Could not allocate a unique key.")

    return ResponseShorten(
        short_url=f"{settings.BASE_URL.rstrip('/')}/{db_url.short_key}",
        custom_key=db_url.short_key,
        long_url=db_url.long_url,
        created_at=db_url.created_at,
        expires_at=db_url.expires_at,
    )