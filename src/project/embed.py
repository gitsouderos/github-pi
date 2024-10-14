from base64 import b64decode
from ollama import Client as ModelClient
from project.config.settings import MODEL_HOST_URL, EMBEDDING_MODEL
from project.config.db import get_session
from project.database_models.content_files import ContentFile as Readme
from project.database_models.embeddings import Embedding
from sqlalchemy.orm import Session

CHAR_LIMIT = 1_700


def nanosec_to_sec(nanosec):
    return nanosec / 1000000000


def get_files(db: Session, offset: int, limit: int = 100) -> list[Readme]:
    try:
        files = (
            db.query(Readme)
            .where(Readme.embedding == None)
            .order_by(Readme.id.asc())
            .offset(offset)
            .limit(limit)
            .all()
        )  # noqa E711
    except Exception as e:
        print(f"[!] ERROR get_files:\n{e.__cause__}")

    return files


def create_embeddings(db: Session, embeddings: list[Embedding]):
    try:
        db.add_all(embeddings)
        db.commit()
    except Exception as e:
        print(f"[!] ERROR inserting Embeddings:\n{e.__cause__}")
        db.rollback()
    print(f"[*] INFO: inserted {len(embeddings)} Embeddings succussfully.")


def generate_embeddings(db: Session, client: ModelClient):
    files_left = 2
    page = 0
    while files_left > 0:
        limit = 50
        files = get_files(db, (page * limit), limit)
        files_left = len(files)
        print(f"[**] INFO: {files_left} CONTENT FILES")
        if files_left == 0:
            pass

        contents = []
        for file in files:
            content = file.content
            if file.encoding == "base64":
                content = b64decode(file.content)
            content = str(content)[:CHAR_LIMIT]
            print(f"[*] INFO: {content[:50]} CONTENT FILES")
            contents.append(content)
            # limited_content = str(content)[:CHAR_LIMIT] # trying with no limit first

        try:
            res = client.embed(model=EMBEDDING_MODEL, keep_alive="5m", input=contents)
            vectors = res["embeddings"]
            seconds = nanosec_to_sec(res.get("total_duration"))
            print(f"[*] INFO: Took {seconds:.2f}s")
        except Exception as e:
            print(f"[!!!] ERROR generating embeddings:\n{e}\n\n")
            pass

        assert len(vectors) == len(files), "Vectors mismatch files!"
        embeddings = []
        for idx, vector in enumerate(vectors):
            f = files[idx]
            embeddings.append(Embedding(embedding=vector, file_id=f.id, file=f))
        create_embeddings(db, embeddings)
        page += 1


if __name__ == "__main__":
    print("=>Started Embeddings for DB's READMEs")
    print(f"[*] INFO: model hosting @ {MODEL_HOST_URL}")
    client = ModelClient(host=MODEL_HOST_URL)
    db_session = next(get_session())

    generate_embeddings(db_session, client)
