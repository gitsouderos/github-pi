from base64 import b64decode
from ollama import Client as ModelClient
from project.config.settings import MODEL_HOST_URL, EMBEDDING_MODEL, CHAR_LIMIT
from project.config.db import get_session
from project.database_models.content_files import ContentFile


def decode_file(readme: ContentFile) -> str:

    if readme.encoding == "base64":
        content = b64decode(readme.content)
    content = str(content)[:CHAR_LIMIT]

    return content


def get_file(file_id: int) -> ContentFile:
    db = next(get_session())
    try:
        file = db.query(ContentFile)\
            .where(ContentFile.id == file_id)\
            .first()  # noqa E711
    except Exception as e:
        print(f"[!] ERROR get_file:\n{e.__cause__}")
        raise

    return file


def generate_embeddings(query: str) -> list[float]:

    client = ModelClient(host=MODEL_HOST_URL)
    query = query[:CHAR_LIMIT]

    try:
        res = client.embed(model=EMBEDDING_MODEL, input=query)
        vectors = res["embeddings"]
    except Exception as e:
        print(f"[!!!] ERROR generating embedding:\n{e}\n\n")
        raise

    return vectors[0]
# TODO: write get cosine similarity etc functions from db
