import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    API_AUTH_KEY: str = os.getenv("API_AUTH_KEY", "dev-secret-key")
    EMBEDDING_MODEL: str = "models/text-embedding-004"
    GENERATION_MODEL: str = "gemini-flash-latest"

settings = Settings()
