from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db
from app.models import User
from app.schemas import UserRegistration, UserLogin, UserResponse, Token
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register(payload: UserRegistration, db: Session = Depends(get_db)):
    email = payload.email
    existing = db.query(User.email).filter(User.email == email).first()

    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with same email already exists")
    user = User(
        email=email,
        pass_hash= hash_password(payload.password),
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return UserResponse(
        email=user.email,
        created_at=user.created_at
    )

@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    email = payload.email
    query = db.query(User.email, User.pass_hash).filter(User.email == email).first()

    if not query:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    if not verify_password(payload.password, query.pass_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    
    access_token = create_access_token(
        data={"sub": query.email}
    )
    return Token(access_token=access_token, token_type="bearer")
