from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.sql import func
from fastapi.responses import RedirectResponse
from datetime import datetime, timezone

from app.database import get_db
from app.models import Url, ClicksAnalytics, User
from app.utils import generate_short_key, calculate_expiration
from app.schemas import RequestShorten, ResponseShorten, UrlListResponse, UrlAnalyticsResponse, DailyClickCount
from app.config import settings
from app.auth import get_optional_user, get_current_user

router = APIRouter()

MAX_KEY_GEN_ATTEMPTS = 5

RESERVED_KEYS = {"admin", "api", "health", "shorten", "docs", "openapi.json", "redoc"}

def _resolve_short_key(payload: RequestShorten, db: Session) -> str:
    if payload.custom_key:
        clean_key = payload.custom_key.lower()
        if clean_key in RESERVED_KEYS:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "This key is reserved.")
        existing = db.query(Url).filter(Url.short_key == clean_key).first()
        if existing:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "This custom key is already taken.")
        return clean_key

    return generate_short_key().lower()

@router.post("/shorten", response_model=ResponseShorten)
def shorten_url(
    payload: RequestShorten,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    is_custom = bool(payload.custom_key)
    key = _resolve_short_key(payload, db)

    attempts = 1 if is_custom else MAX_KEY_GEN_ATTEMPTS
    for attempt in range(attempts):
        db_url = Url(
            long_url=str(payload.long_url),
            short_key=key,
            expires_at=calculate_expiration(payload.expiration_days),
            user_id=current_user.id if current_user else None
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
            key = generate_short_key().lower()
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Could not allocate a unique key.")

    return ResponseShorten(
        short_url=f"{settings.BASE_URL.rstrip('/')}/{db_url.short_key}",
        custom_key=db_url.short_key,
        long_url=db_url.long_url,
        created_at=db_url.created_at,
        expires_at=db_url.expires_at,
    )


@router.get("/{short_key}")
def redirect_short_url(short_key: str, request: Request, db: Session = Depends(get_db)):
    clean_key = short_key.lower()

    url = db.query(Url.long_url, Url.expires_at, Url.id).filter(Url.short_key == clean_key).first()

    if not url:  
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such url exists"
        )

    if url.expires_at and datetime.now(timezone.utc) >= url.expires_at:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="The Url has expired"
        )
    
    user_agent_string = request.headers.get("user-agent", "Unknown")
    referrer_string = request.headers.get("referer", None)    
    click = ClicksAnalytics(
        url_id=url.id,
        user_agent=user_agent_string[:511],
        country_code="XX",                 
        referrer=referrer_string[:2048] if referrer_string else None
    )
    try:
        db.add(click)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
    return RedirectResponse(url=url.long_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

@router.get("/user/urls", response_model=list[UrlListResponse])
def get_user_urls(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    urls = db.query(Url).filter(Url.user_id == current_user.id).all()
    return [UrlListResponse(
        url_id=url.id,
        long_url=url.long_url,
        short_key=url.short_key,
        created_at=url.created_at,
        expires_at=url.expires_at
    ) for url in urls]

@router.get("/urls/{url_id}/analytics", response_model=UrlAnalyticsResponse)
def get_url_analytics(url_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    valid_req = db.query(Url).filter(Url.id == url_id, Url.user_id == current_user.id).first()

    if valid_req is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    total_clicks = db.query(ClicksAnalytics).filter(ClicksAnalytics.url_id == url_id).count()

    daily_counts = (
        db.query(
            func.date(ClicksAnalytics.clicked_at).label("day"),
            func.count().label("count")
        )
        .filter(ClicksAnalytics.url_id == url_id)
        .group_by(func.date(ClicksAnalytics.clicked_at))
        .all()
    )
    return UrlAnalyticsResponse(
        url_id=url_id,
        short_key=valid_req.short_key,
        total_clicks=total_clicks,
        daily_breakdown=[
            DailyClickCount(date=row.day, count=row.count) for row in daily_counts
        ]
    )