from project.config.settings import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from typing import Any, Generator


sync_engine = create_engine(
    DATABASE_URL,
    pool_size=15,
    max_overflow=20,
    pool_timeout=60,
)


def get_session() -> Generator[Session, Any, None]:
    """
    Creates and yields a SQLAlchemy Session object.
    This function is a generator that creates a new SQLAlchemy Session
    using the global `sync_engine`. It yields the session and ensures
    that it's properly closed after use.

    Returns:
        Generator[Session, Any, None]: A generator yielding a SQLAlchemy Session.

    Usage:
        To use this function, you can either:
        1. Use it in a for loop (recommended for automatic cleanup):
            for db in get_session():
                # Use db here
                results = db.query(TableModel).all()
        2. Use next() to get the session directly:
            db = next(get_session())
            # Remember to close the session manually in this case
    Example:
        # Using method 1 (recommended)
        for db in get_session():
            users = db.query(User).filter(User.age > 18).all()
            for user in users:
                print(user.name)
        # Using method 2
        db = next(get_session())
        try:
            products = db.query(Product).filter(Product.price < 100).all()
            for product in products:
                print(product.name, product.price)
        finally:
            db.close()  # Make sure to close the session
    Note:
        When using method 2, always remember to close the session manually
        to prevent resource leaks.
    """
    with Session(sync_engine) as session:
        yield session
