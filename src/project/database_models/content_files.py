from typing import TYPE_CHECKING
from base64 import b64decode
from project.database_models.base import Base
if TYPE_CHECKING:
    from project.database_models.embeddings import Embedding
from sqlalchemy import Index, Integer, String, Text, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, class_mapper, relationship
from github.ContentFile import ContentFile as GithubContentFile
from project.config.settings import CHAR_LIMIT


class ContentFile(Base):
    __tablename__ = "content_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type_of: Mapped[str] = mapped_column(String)  # WARN: og name was type
    encoding: Mapped[str] = mapped_column(String)
    size: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)
    path: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(Text)
    sha: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    git_url: Mapped[str] = mapped_column(String)
    html_url: Mapped[str] = mapped_column(String)
    download_url: Mapped[str] = mapped_column(String)

    embedding: Mapped["Embedding"] = relationship(back_populates="file")

    repository_id: Mapped[int] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE")
    )

    __table_args__ = (Index("content_files_name", name),)

    def get_content(self, truncate: bool = False) -> str:
        content = self.content

        if self.encoding == "base64":
            content = b64decode(self.content).decode("utf-8")

        return content if truncate else content[:CHAR_LIMIT]

    def __repr__(self):
        return (
            f"ContentFile("
            f"id={self.id}, "
            f"name={self.name!r}, "
            f"size={self.size!r}, "
            f"content={b64decode(self.content)[:20]!r}, "
            f"inserted_at={self.inserted_at}, "
            f")"
        )

    @classmethod
    def from_instance(cls, file: GithubContentFile):

        obj_data = file.raw_data
        obj_data["repository_id"] = file.repository.id
        obj_data["type_of"] = file.type

        valid_keys = {prop.key for prop in class_mapper(cls).iterate_properties}
        valid_data = {k: v for k, v in obj_data.items() if k in valid_keys}

        return cls(**valid_data)

    @classmethod
    def from_dict(cls, obj_data: dict[str, any]):

        valid_keys = {prop.key for prop in class_mapper(cls).iterate_properties}
        valid_data = {k: v for k, v in obj_data.items() if k in valid_keys and v is not None}

        return cls(**valid_data)
