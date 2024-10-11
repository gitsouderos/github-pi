import psycopg
from sqlalchemy.exc import SQLAlchemyError
from project.config.db import sync_engine
from project.config.settings import DATABASE_URL

print(f"db url: {DATABASE_URL}")


def test_sqlalchemy_connection():
    try:
        with sync_engine.connect() as connection:
            result = connection.execute("SELECT version();")
            version = result.scalar()
            print("Successfully connected to the database using SQLAlchemy")
            print(f"PostgreSQL version: {version}")
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error: {e}")


def test_psycopg_connection():
    psycopg_url = "postgresql://postgres:postgres@db:5432/data_db"
    try:
        with psycopg.connect(psycopg_url) as conn:
            print("Successfully connected to the database using psycopg3!")
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()[0]
                print(f"PostgreSQL version: {version}")
    except psycopg.OperationalError as e:
        print(f"psycopg3 OperationalError: {e}")
    except Exception as e:
        print(f"An error occurred with psycopg3: {e}")


if __name__ == "__main__":
    print("Testing SQLAlchemy connection:")
    test_sqlalchemy_connection()
    print("\nTesting psycopg3 connection:")
    test_psycopg_connection()
# session = get_session()
# session.close()
print("SUCCESS")
