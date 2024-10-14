from time import sleep
from sqlalchemy import create_engine
from sqlalchemy.orm import joinedload
from project.config.db import get_session
from psycopg.errors import UniqueViolation

from sqlalchemy.orm import Session, sessionmaker
from project.database_models.repositories import Repository as RepositoryModel
from project.database_models.organizations import Organization as OrganizationModel
from project.database_models.users import User as UserModel
from project.database_models.languages import Language as LanguageModel
from project.database_models.content_files import ContentFile as ContentFileModel


def insert_org(db: Session, org: OrganizationModel):
    try:
        db.add(org)
        db.commit()
        db.refresh(org)
    except Exception as e:
        if not isinstance(e, UniqueViolation):
            print(f"[!] ERROR inserting Orangization:\n{e.__cause__}")
        db.rollback()
    finally:
        db.close()
    return org


def insert_user(db: Session, user: UserModel):
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        if not isinstance(e, UniqueViolation):
            print(f"[!] ERROR inserting User:\n{e.__cause__}")
        db.rollback()
    finally:
        db.close()
    return user


def insert_repo(db: Session, repo: RepositoryModel):
    try:
        db.add(repo)
        db.commit()
        db.refresh(repo)
    except Exception as e:
        if not isinstance(e, UniqueViolation):
            print(f"[!] ERROR inserting Repo:\n{e}")
        db.rollback()
    finally:
        db.close()
    return repo


def get_anand_sesh() -> Session:
    secondary_engine = create_engine(
        "postgresql+psycopg://postgres:postgres@db:5432/postgres",
        pool_size=15,
        max_overflow=25,
        pool_timeout=60,
    )
    SessionLocal = sessionmaker(bind=secondary_engine)
    return SessionLocal()


def get_anand_repos() -> list[RepositoryModel]:
    sesh = get_anand_sesh()
    try:
        repos = (
            sesh.query(RepositoryModel)
            .where(RepositoryModel.stargazers_count < 804)
            .order_by(RepositoryModel.stargazers_count.desc())
            .options(joinedload(RepositoryModel.languages))
            .all()
        )
        sesh.expunge_all()
    except Exception as e:
        print(f"[!] ERROR get_anand_repo:\n{e.__cause__}")
    finally:
        sesh.close()

    return repos


def get_anand_org(org_id: int) -> OrganizationModel:
    sesh = get_anand_sesh()
    try:
        org = (
            sesh.query(OrganizationModel).where(OrganizationModel.id == org_id).first()
        )
        if org is not None:
            sesh.expunge(org)
    except Exception as e:
        print(f"[!] ERROR get_anand_org:\n{e.__cause__}")
    finally:
        sesh.close()

    return org


def get_anand_repo(repo_id: int) -> RepositoryModel:
    sesh = get_anand_sesh()
    try:
        repo = sesh.query(RepositoryModel).where(RepositoryModel.id == repo_id).first()
        if repo is not None:
            sesh.expunge(repo)
    except Exception as e:
        print(f"[!] ERROR get_anand_repo:\n{e.__cause__}")
    finally:
        sesh.close()

    return repo


def get_anand_user(uid: int) -> UserModel:
    sesh = get_anand_sesh()
    try:
        user = sesh.query(UserModel).where(UserModel.id == uid).first()
        if user is not None:
            sesh.expunge(user)
    except Exception as e:
        print(f"[!] ERROR get_anand_user:\n{e.__cause__}")
    finally:
        sesh.close()

    return user


def get_anand_readme(repo_id: int) -> ContentFileModel:
    sesh = get_anand_sesh()
    try:
        readme = (
            sesh.query(ContentFileModel)
            .where(ContentFileModel.repository_id == repo_id)
            .first()
        )
        if readme is not None:
            sesh.expunge(readme)
    except Exception as e:
        print(f"[!] ERROR getanandreadme:\n{e.__cause__}")
    finally:
        sesh.close()

    return readme


def collect_data(db_main: Session):
    repos = get_anand_repos()
    anand_total = len(repos)
    print(f"TOTAL COUNT: {anand_total}")

    idx = 0
    for repo in repos:
        idx += 1
        if idx % 100 == 0:
            sleep(1)
        print(
            f"\n[*] INFO: ({idx}/{anand_total}): {repo.full_name}, stars: {repo.stargazers_count}"
        )
        # pesky rule 1:
        readme = get_anand_readme(repo.id)
        if readme is not None:
            readme.id = None
            repo.readme = ContentFileModel.from_dict(readme.__dict__)

        # pesky rule 2:
        for i, lang in enumerate(repo.languages):
            lang.id = None
            repo.languages[i] = LanguageModel.from_dict(lang.__dict__)

        if repo.organization_id is not None:
            org = get_anand_org(repo.organization_id)
            insert_org(db_main, OrganizationModel.from_dict(org.__dict__))

        if repo.parent_id is not None:
            parent_repo_model = get_anand_repo(repo.parent_id)
            insert_repo(db_main, RepositoryModel.from_dict(parent_repo_model.__dict__))

        if repo.owner_id > 0:
            owner = get_anand_user(repo.owner_id)
            insert_user(db_main, UserModel.from_dict(owner.__dict__))

        insert_repo(db_main, RepositoryModel.from_dict(repo.__dict__))


if __name__ == "__main__":
    print("=>Started Merge")
    db_session = next(get_session())
    failure_count = collect_data(db_session)
