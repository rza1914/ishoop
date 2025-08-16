from pydantic_settings import BaseSettings
from typing import Optional, List
import secrets

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "iShop"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "iShop - Modern E-commerce API"
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./ishop.db"
    
    # Security Configuration
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # CORS Configuration
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "0.0.0.0"]
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]
    
    # Redis Configuration (Optional)
    REDIS_URL: Optional[str] = None
    CACHE_EXPIRE_SECONDS: int = 3600  # 1 hour
    
    # Email Configuration (Optional)
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = 587
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # OAuth Configuration (Optional)
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    ADMIN_TELEGRAM_IDS: Optional[str] = None
    API_BASE_URL: str = "http://localhost:8000"
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp", "application/pdf"]
    UPLOAD_DIRECTORY: str = "app/static/uploads"
    
    # Pagination Configuration
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Rate Limiting Configuration
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
