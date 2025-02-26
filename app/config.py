import os
from pydantic_settings import BaseSettings


class Config:
    TEMP_PDF_PATH = "/tmp/pdf_uploads" 

class Settings(BaseSettings):
    DB_HOST: str = os.getenv("DB_HOST", "mysql")
    DB_USER: str = os.getenv("DB_USER", "app_user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "app_password")
    DB_NAME: str = os.getenv("DB_NAME", "app_db")
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://mongo:27017")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecretkey")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

settings = Settings()
