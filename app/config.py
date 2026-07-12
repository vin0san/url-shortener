import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres@localhost:5432/url_production")
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")

settings = Settings()