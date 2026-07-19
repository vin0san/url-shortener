import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres@localhost:5432/url_production")
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY not set — check your .env file")

settings = Settings()