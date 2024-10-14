from project.database_models.base import Base
from sqlalchemy import ForeignKey, Index, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, class_mapper


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    num_bytes: Mapped[int] = mapped_column(Integer)
    repository_id: Mapped[int] = mapped_column(ForeignKey("repositories.id"))

    __table_args__ = (
        Index("languages_repo_id", repository_id),
        Index("languages_name", name),
    )

    def __repr__(self):
        return f"Language(id={self.id!r}, name={self.name!r}, repository_id={self.repository_id!r})"

    @classmethod
    def from_dict(cls, obj_data: dict[str, any]):
        valid_keys = {prop.key for prop in class_mapper(cls).iterate_properties}
        valid_data = {
            k: v for k, v in obj_data.items() if k in valid_keys and v is not None
        }

        return cls(**valid_data)
