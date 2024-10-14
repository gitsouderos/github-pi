import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
MODEL_HOST_URL = os.getenv("MODEL_HOST_URL")
EMBEDDING_MODEL = (
    "bge-m3"  # WARN: changing this will might change the vector size in the db
)
CHAR_LIMIT = 1_700  # WARN: changing this will make db embeddings not match
