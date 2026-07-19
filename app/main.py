from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.database import get_db
from app.routes import router
from app.auth_routes import router as auth_router

app = FastAPI(title="Url Shortener", version="1.0")

@app.get("/")
def root():
    return {"App": "Url Shortener", "Version": "1.0"}

@app.get("/health")
def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected", "version": "1.0"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {str(e)}"
        )

app.include_router(auth_router)
app.include_router(router)