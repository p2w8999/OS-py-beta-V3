
import os


class Config:
    SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT = int(os.getenv("SERVER_PORT", 5000))
    DATABASE_PATH = os.getenv("DATABASE_PATH", "./storage/database.db")
    STORAGE_ROOT = os.getenv("STORAGE_ROOT", "./storage")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"


config = Config()
