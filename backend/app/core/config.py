import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "YourTeacher API"
    API_V1_STR: str = "/api"  # Changed from /api/v1 to /api to match frontend
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    # In production, use a real DB URL
    DATABASE_URL: str = "sqlite+aiosqlite:///./yourteacher.db"

settings = Settings()


