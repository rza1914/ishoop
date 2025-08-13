from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "iShop"
    
    # Database - SQLite برای Windows
    DATABASE_URL: str = "sqlite:///./ishop.db"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production-please-make-it-very-long-and-random"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Redis (Optional for Windows)
    REDIS_URL: Optional[str] = None
    
    # Email (Optional)
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()
