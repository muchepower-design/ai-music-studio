import os
from dotenv import load_dotenv

# Load .env file if exists
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/musicstudio")
STORAGE_PATH = os.getenv("STORAGE_PATH", "./storage")
MODEL_CACHE = os.getenv("MODEL_CACHE", "./model_cache")