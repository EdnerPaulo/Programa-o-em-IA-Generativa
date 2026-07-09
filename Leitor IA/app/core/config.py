from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    GEMINI_API_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    MAX_FILE_SIZE_BYTES: int = 15 * 1024 * 1024  # 15MB
    UPLOAD_DIR: str = "./uploads"

    model_config = ConfigDict(env_file=".env", extra="ignore")

settings = Settings()