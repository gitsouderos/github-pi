from datetime import datetime
from typing import Optional, List
from github.Organization import Organization as GithubOrganization
from project.database_models.base import Base
from project.database_models.repositories import Repository
from sqlalchemy import Integer, String, Boolean, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship, class_mapper


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    repositories: Mapped[List["Repository"]] = relationship()
    login: Mapped[str] = mapped_column(String)
    node_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    repos_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    events_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    hooks_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    issues_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    members_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    public_members_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    company: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    blog: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    twitter_username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_verified: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    has_organization_projects: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    has_repository_projects: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    public_repos: Mapped[int] = mapped_column(Integer)
    public_gists: Mapped[int] = mapped_column(Integer)
    followers: Mapped[int] = mapped_column(Integer)
    following: Mapped[int] = mapped_column(Integer)
    html_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    type_of: Mapped[str] = mapped_column(
        String
    )  # WARN: OG name is type which is reserved
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)
    archived_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        Index("orangization_login", login),
        Index("orangization_name", name),
        Index("organization_company", company),
    )

    @classmethod
    def from_instance(cls, org: GithubOrganization):

        obj_data = org.raw_data
        obj_data["type_of"] = org.type

        valid_keys = {prop.key for prop in class_mapper(cls).iterate_properties}
        valid_data = {k: v for k, v in obj_data.items() if k in valid_keys}

        return cls(**valid_data)

    @classmethod
    def from_dict(cls, obj_data: dict[str, any]):

        valid_keys = {prop.key for prop in class_mapper(cls).iterate_properties}
        valid_data = {k: v for k, v in obj_data.items() if k in valid_keys and v is not None}

        return cls(**valid_data)

