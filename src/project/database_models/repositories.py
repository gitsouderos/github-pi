from datetime import datetime
from typing import List, Optional
from project.database_models.languages import Language
from project.database_models.content_files import ContentFile
from project.database_models.base import Base
from sqlalchemy import String, Boolean, Integer, JSON, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship, class_mapper
from github.Repository import Repository as GithubRepository


class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)

    allow_auto_merge: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    allow_forking: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    allow_merge_commit: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    allow_rebase_merge: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    allow_squash_merge: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    allow_update_branch: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    archived: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    archive_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    assignees_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    blobs_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    branches_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    clone_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    collaborators_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    comments_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    commits_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    compare_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    contents_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    contributors_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    default_branch: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    delete_branch_on_merge: Mapped[Optional[bool]] = mapped_column(
        Boolean, nullable=True
    )
    deployments_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    downloads_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    events_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    fork: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    forks: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    forks_count: Mapped[int] = mapped_column(Integer)
    forks_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    full_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    git_commits_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    git_refs_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    git_tags_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    git_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    has_downloads: Mapped[[Boolean]] = mapped_column(Boolean, nullable=True)
    has_issues: Mapped[bool] = mapped_column(Boolean)
    has_pages: Mapped[bool] = mapped_column(Boolean)
    has_projects: Mapped[bool] = mapped_column(Boolean)
    has_wiki: Mapped[bool] = mapped_column(Boolean)
    has_discussions: Mapped[bool] = mapped_column(Boolean)
    homepage: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    hooks_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    html_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_template: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    issue_comment_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    issue_events_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    issues_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    keys_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    labels_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    language: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    languages_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    languages: Mapped[List["Language"]] = relationship()
    merge_commit_message: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    merge_commit_title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    merges_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    milestones_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    mirror_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String)
    network_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    notifications_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    open_issues: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    open_issues_count: Mapped[int] = mapped_column(Integer)
    organization_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("organizations.id"), nullable=True
    )
    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("repositories.id"), nullable=True)
    # permissions: Deleted because of no documentations
    private: Mapped[bool] = mapped_column(Boolean)
    pulls_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    pushed_at: Mapped[datetime] = mapped_column(DateTime)
    releases_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    # security_and_analysis: removed
    size: Mapped[int] = mapped_column(Integer)
    squash_merge_commit_message: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )
    squash_merge_commit_title: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )
    ssh_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    stargazers_count: Mapped[Optional[int]] = mapped_column(Integer)
    stargazers_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    statuses_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    subscribers_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    subscribers_count: Mapped[Optional[int]] = mapped_column(Integer)
    subscription_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    svn_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    tags_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    teams_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    topics: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    trees_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    web_commit_signoff_required: Mapped[Optional[bool]] = mapped_column(Boolean)
    cluster: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    readme: Mapped[Optional["ContentFile"]] = relationship()

    __table_args__ = (
        Index("repo_fullname", full_name),
        Index("repo_organization_id", organization_id),
        Index("repo_parent_id", parent_id),
        Index("repo_size", size),
    )

    def __repr__(self):
        return (
            f"Repository("
            f"id={self.id}, "
            f"name={self.name!r}, "
            f"full_name={self.full_name!r}, "
            f"created_at={self.created_at}, "
            f"default_branch={self.default_branch!r}, "
            f"clone_url={self.clone_url!r}, "
            f"fork={self.fork}, "
            f"..."
            f"forks_count={self.forks_count}, "
            f"open_issues_count={self.open_issues_count}, "
            f"stargazers_count={self.stargazers_count}, "
            f"size={self.size}, "
            f"updated_at={self.updated_at}, "
            f"language={self.language}, "
            f"languages={self.languages}, "
            f"private={self.private}"
            f")"
        )

    @classmethod
    def from_instance(cls, repo: GithubRepository):

        obj_data = repo.raw_data

        if repo.organization:
            obj_data["organization_id"] = repo.organization.id
        if repo.parent:
            obj_data["parent_id"] = repo.parent.id
        if repo.owner:
            obj_data["owner_id"] = repo.owner.id
        try:
            content_file = repo.get_readme()
            obj_data["readme"] = ContentFile.from_instance(content_file)
        except Exception as e:
            print(f"Warning: Failed to fetch readme,\n{e}")

        try:
            obj_data["languages"] = [
                    Language(name=name,
                             num_bytes=num_bytes,
                             repository_id=repo.id)
                    for name, num_bytes in repo.get_languages().items()]
        except Exception as e:
            print(f"Warning: Failed to fetch languages,\n{e}")

        valid_keys = {prop.key for prop in class_mapper(cls).iterate_properties}
        valid_data = {k: v for k, v in obj_data.items() if k in valid_keys}

        return cls(**valid_data)

    @classmethod
    def from_dict(cls, obj_data: dict[str, any]):

        valid_keys = {prop.key for prop in class_mapper(cls).iterate_properties}
        valid_data = {k: v for k, v in obj_data.items() if k in valid_keys and v is not None}

        return cls(**valid_data)
