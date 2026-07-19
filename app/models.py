from sqlalchemy import Column, String, BigInteger, DateTime, CHAR, ForeignKey, VARCHAR
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    pass_hash = Column(VARCHAR(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    urls = relationship("Url", back_populates="user")

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"
    

class Url(Base):
    __tablename__ = "urls"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), default=None, nullable=True)
    long_url = Column(String(2048), nullable=False)
    short_key = Column(String(10), nullable=False, unique=True, index=True)
    
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="urls")
    clicks = relationship("ClicksAnalytics", back_populates="url")

    def __repr__(self):
        return f"<Url short_key={self.short_key}>"



class ClicksAnalytics(Base):
    __tablename__ = "clicks_analytics"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    clicked_at = Column(DateTime(timezone=True), server_default=func.now())
    user_agent = Column(String, nullable=True)
    country_code = Column(CHAR(2), nullable=True)
    referrer = Column(String)
    
    url_id = Column(BigInteger, ForeignKey("urls.id", ondelete="CASCADE"))

    url = relationship("Url", back_populates="clicks")

    def __repr__(self):
        return f"<ClicksAnalytics id={self.id} country={self.country_code}>"