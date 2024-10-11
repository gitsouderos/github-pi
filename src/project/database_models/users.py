from datetime import datetime
from typing import Optional, List
from github.NamedUser import NamedUser as GithubNamedUser
from project.database_models.base import Base
from project.database_models.repositories import Repository
from sqlalchemy import Integer, String, Boolean, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship, class_mapper


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    node_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    gravatar_id: Mapped[str] = mapped_column(String, default="")
    url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    html_url: Mapped[str] = mapped_column(String)
    followers_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    following_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    gists_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    starred_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    subscriptions_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    organizations_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    repos_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    repos: Mapped[List["Repository"]] = relationship()
    events_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    received_events_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    type_of: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # WARN: changed from type since its reserverd
    site_admin: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    company: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    blog: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    hireable: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    twitter_username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    public_repos: Mapped[int] = mapped_column(Integer)
    public_gists: Mapped[int] = mapped_column(Integer)
    followers: Mapped[int] = mapped_column(Integer)
    following: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        Index("user_name", name),
        Index("company_name", company),
    )

    @classmethod
    def from_instance(cls, user: GithubNamedUser):

        obj_data = user.raw_data
        obj_data["type_of"] = user.type

        valid_keys = {prop.key for prop in class_mapper(cls).iterate_properties}
        valid_data = {k: v for k, v in obj_data.items() if k in valid_keys}

        return cls(**valid_data)

    @classmethod
    def from_dict(cls, obj_data: dict[str, any]):

        valid_keys = {prop.key for prop in class_mapper(cls).iterate_properties}
        valid_data = {k: v for k, v in obj_data.items() if k in valid_keys and v is not None}

        return cls(**valid_data)

    def __repr__(self):
        return (
            f"User("
            f"id={self.id}, "
            f"name={self.name!r}, "
            f"name={self.email!r}, "
            f")"
        )
