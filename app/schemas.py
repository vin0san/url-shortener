from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field, StringConstraints, EmailStr
from typing import Annotated

ValidCustomKey = Annotated[
    str, 
    StringConstraints(pattern=r"^[a-zA-Z0-9_-]+$", min_length=3, max_length=10)
]

ValidPassword = Annotated[
    str, 
    StringConstraints(min_length=8, max_length=128)
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

class UserRegistration(BaseModel):
    email: EmailStr
    password: ValidPassword

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str