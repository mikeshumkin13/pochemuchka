import os
from pydantic import BaseModel

class Settings(BaseModel):
    api_secret: str = os.getenv("API_SECRET", "dev")
    db_dsn: str = os.getenv("DB_DSN", "postgresql+psycopg://user:pass@db:5432/pochemuchka")
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    moderation_enabled: bool = os.getenv("MODERATION_ENABLED", "true").lower() == "true"

settings = Settings()


