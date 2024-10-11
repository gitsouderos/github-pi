from project.config.settings import DATABASE_URL, EMBEDDING_MODEL, MODEL_HOST_URL
from project.config.db import get_session
from sql

print("Your settings:")
print(f"db url: '{DATABASE_URL}'")
print(f"embed with: '{EMBEDDING_MODEL}'")
print(f"model host: '{MODEL_HOST_URL}'\n\n")

db = next(get_session())
print("DB up?")
db.

print("TODO: our main functionality")
