from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field, StringConstraints
from typing import Annotated

# Enforces alphanumeric characters only, no spaces, max 15 chars (Prevents: $$$, admin spaces)
ValidCustomKey = Annotated[
    str, 
    StringConstraints(pattern=r"^[a-zA-Z0-9_-]+$", min_length=3, max_length=10)
]

class RequestShorten(BaseModel):
    long_url: HttpUrl
    custom_key: ValidCustomKey | None = None
    expiration_days: int | None = Field(default=30, ge=1, le=365)

class ResponseShorten(BaseModel):
    short_url: str
    custom_key: str
    long_url: str
    created_at: datetime
    expires_at: datetime | None