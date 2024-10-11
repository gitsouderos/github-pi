from typing import TYPE_CHECKING
from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from project.database_models.base import Base
if TYPE_CHECKING:
    from project.database_models.content_files import ContentFile


class Embedding(Base):
    """
    We are using bge-m3 for embedding readme files.
      Model
        architecture        bert
        parameters          566.70M
        context length      8192
        embedding length    1024
        quantization        F16
      License
        MIT License
        Copyright (c) [year] [fullname]
    """

    __tablename__ = "embeddings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    embedding: Mapped[Vector] = mapped_column(Vector(1024))
    file_id: Mapped[int] = mapped_column(ForeignKey("content_files.id"))
    file: Mapped["ContentFile"] = relationship(back_populates="embedding")
