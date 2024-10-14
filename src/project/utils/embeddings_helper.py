from base64 import b64decode
from ollama import Client as ModelClient
from project.config.settings import MODEL_HOST_URL, EMBEDDING_MODEL, CHAR_LIMIT
from project.config.db import get_session
from project.database_models.content_files import ContentFile
from project.database_models.repositories import Repository
from sqlalchemy import select


def log_error(msg: str):
    print(f"[!] ERROR:\n{msg}\n")


def decode_file(readme: ContentFile) -> str:
    """Legacy now. Just use content_file_instance.get_content()"""
    return readme.get_content()


def get_file(file_id: int) -> ContentFile:
    db = next(get_session())
    try:
        file = db.query(ContentFile)\
            .where(ContentFile.id == file_id)\
            .first()  # noqa E711
    except Exception as e:
        log_error(e.__cause__)
        raise

    return file


def generate_embeddings(query: str) -> list[float]:

    client = ModelClient(host=MODEL_HOST_URL)
    query = query[:CHAR_LIMIT]

    try:
        res = client.embed(model=EMBEDDING_MODEL, input=query)
        vectors = res["embeddings"]
    except Exception as e:
        log_error(f"Error in generate_embeddings:\n{e}")
        raise

    return vectors[0]


def get_similar_repos(query: str, limit: int = 5) -> list[Repository]:
    """Gets most similar repostiories by cosine similarity"""
    db = next(get_session())

    try:
        query_vector = generate_embeddings(query)
        stmt = (select(Repository)
                .order_by(
                    Repository
                    .readme
                    .embedding
                    .embedding
                    .cosine_distance(query_vector)
                    )
                .limit(limit))

        return db.scalars(stmt).all()
    except Exception as e:
        print(f"[!!!] ERROR generating embedding:\n{e}\n\n")


def do_the_thing(
        query: str,
        cluster_limit: int = 5
) -> list[Repository]:
    """
    Do it all. Get similar repos from query
        -> Get repos in cluster
            -> Finally return most similar Repos in cluster
            (ranked by cosine similarity to user query).
    """
    db = next(get_session())
    query_vector = generate_embeddings(query)

    try:
        most_similar_repo = db.query(Repository)\
                .order_by(
                        Repository.readme
                        .embedding.embedding
                        .cosine_similarity(query_vector)
                        )\
                .limit(1)\
                .first()

        stmt = (
                select(Repository)
                .where(Repository.cluster == most_similar_repo.cluster)
                .order_by(Repository)
                .limit(cluster_limit)
                )
        return db.scalars(stmt).all()
    except Exception as e:
        print(f"[!!!] ERROR generating embedding:\n{e}\n\n")
